import os
import json
import time
import uuid
import threading
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# =============================
# ENV CONFIG
# =============================
API_KEY = os.getenv("GS_API_KEY", "GOLD_SNIPER_VIP_SN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
STORE_FILE = os.getenv("STORE_FILE", "signal_store.json")
MAX_BOOKMAP_AGE_SEC = int(float(os.getenv("MAX_BOOKMAP_AGE_SEC", "86400")))
MAX_HISTORY = int(float(os.getenv("MAX_HISTORY", "200")))
REQUEST_TIMEOUT_SEC = int(float(os.getenv("REQUEST_TIMEOUT_SEC", "10")))

_lock = threading.RLock()

DEFAULT_STORE = {
    "bookmap_latest": None,
    "signal_latest": None,
    "discord_latest": None,
    "history": []
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_store() -> Dict[str, Any]:
    if not os.path.exists(STORE_FILE):
        return dict(DEFAULT_STORE)
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in DEFAULT_STORE.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return dict(DEFAULT_STORE)


def save_store(data: Dict[str, Any]) -> None:
    tmp = STORE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STORE_FILE)


def get_payload() -> Dict[str, Any]:
    if request.is_json:
        payload = request.get_json(silent=True) or {}
    else:
        raw = request.get_data(as_text=True) or ""
        try:
            payload = json.loads(raw) if raw.strip() else {}
        except Exception:
            payload = {"raw_text": raw}
    if not isinstance(payload, dict):
        payload = {"raw": payload}
    return payload


def auth_ok(payload: Optional[Dict[str, Any]] = None) -> bool:
    if not API_KEY:
        return True
    q_key = request.args.get("key", "")
    h_key = request.headers.get("X-API-Key", "")
    p_key = ""
    if payload:
        p_key = str(payload.get("key") or payload.get("api_key") or "")
    return API_KEY in {q_key, h_key, p_key}


def pick_float(payload: Dict[str, Any], *keys: str) -> Optional[float]:
    for key in keys:
        value = payload.get(key)
        if value is None or value == "":
            continue
        try:
            return float(str(value).replace(",", ""))
        except Exception:
            pass
    return None


def pick_text(payload: Dict[str, Any], *keys: str, default: str = "-") -> str:
    for key in keys:
        value = payload.get(key)
        if value is not None and str(value) != "":
            return str(value)
    return default


def normalize_event(payload: Dict[str, Any], source_name: str) -> Dict[str, Any]:
    price = pick_float(payload, "price", "gold_price", "entry", "close", "current", "last")
    event = {
        "id": str(payload.get("signal_id") or payload.get("id") or f"{source_name}_{int(time.time()*1000)}_{uuid.uuid4().hex[:6]}"),
        "source": source_name,
        "received_at": now_iso(),
        "received_ts": time.time(),
        "symbol": pick_text(payload, "symbol", "ticker", default="XAUUSD"),
        "signal": pick_text(payload, "signal", "side", "flow", "type", default="INFO").upper(),
        "side": pick_text(payload, "side", "signal", default="-").upper(),
        "type": pick_text(payload, "type", "event", default=source_name.upper()),
        "timeframe": pick_text(payload, "timeframe", "tf", default="-"),
        "price": price,
        "entry": pick_float(payload, "entry"),
        "sl": pick_float(payload, "sl", "stop_loss"),
        "tp1": pick_float(payload, "tp1"),
        "tp2": pick_float(payload, "tp2"),
        "tp3": pick_float(payload, "tp3"),
        "score": pick_text(payload, "score", "buyScore", "sellScore", default="-"),
        "heatmap": pick_text(payload, "heatmap", "flow", default="-"),
        "raw": payload,
    }
    return event


def age_text(event: Optional[Dict[str, Any]]) -> str:
    if not event:
        return "ไม่มีข้อมูล"
    sec = max(0, int(time.time() - float(event.get("received_ts", time.time()))))
    if sec < 60:
        return f"{sec}s ago"
    if sec < 3600:
        return f"{sec//60}m ago"
    return f"{sec//3600}h {(sec%3600)//60}m ago"


def fmt_price(v: Any) -> str:
    if v is None or v == "":
        return "-"
    try:
        return f"{float(v):,.2f}"
    except Exception:
        return str(v)


def build_discord_embed(signal: Dict[str, Any], bookmap: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    sig = signal.get("signal", "INFO")
    side = signal.get("side") if signal.get("side") != "-" else sig
    color = 0x22C55E if "BUY" in sig else 0xEF4444 if "SELL" in sig else 0xF59E0B

    sig_price = signal.get("entry") or signal.get("price")
    bm_price = bookmap.get("price") if bookmap else None
    ref_price = sig_price or bm_price

    bookmap_ok = bool(bookmap)
    bookmap_fresh = bookmap_ok and (time.time() - float(bookmap.get("received_ts", 0)) <= MAX_BOOKMAP_AGE_SEC)
    confirm = "✅ CONFIRM" if bookmap_fresh and bookmap and str(bookmap.get("signal", "")).upper().find(str(side).upper()) >= 0 else "⚠️ CHECK"

    desc = (
        f"**Signal:** `{sig}` | **Side:** `{side}`\n"
        f"**Symbol:** `{signal.get('symbol','XAUUSD')}` | **TF:** `{signal.get('timeframe','-')}`\n"
        f"**Reference Price:** `{fmt_price(ref_price)}`\n"
        f"**Bookmap Match:** {confirm}"
    )

    fields = [
        {"name": "🎯 Trade Signal", "value": (
            f"Entry: `{fmt_price(signal.get('entry') or signal.get('price'))}`\n"
            f"SL: `{fmt_price(signal.get('sl'))}`\n"
            f"TP1: `{fmt_price(signal.get('tp1'))}`\n"
            f"TP2: `{fmt_price(signal.get('tp2'))}`\n"
            f"TP3: `{fmt_price(signal.get('tp3'))}`\n"
            f"ID: `{signal.get('id')}`"
        ), "inline": True},
        {"name": "📊 Latest Bookmap / Orderflow", "value": (
            f"Status: `{bookmap.get('signal','-') if bookmap else '-'}`\n"
            f"Type: `{bookmap.get('type','-') if bookmap else '-'}`\n"
            f"TF: `{bookmap.get('timeframe','-') if bookmap else '-'}`\n"
            f"Score: `{bookmap.get('score','-') if bookmap else '-'}`\n"
            f"Heatmap: `{bookmap.get('heatmap','-') if bookmap else '-'}`\n"
            f"Price: `{fmt_price(bm_price)}`\n"
            f"Age: `{age_text(bookmap)}`"
        ), "inline": True},
    ]

    return {
        "username": "Gold Sniper AI",
        "avatar_url": "https://i.imgur.com/7QfZ8yA.png",
        "embeds": [{
            "title": "🥇 GOLD SNIPER AI SIGNAL + BOOKMAP",
            "description": desc,
            "color": color,
            "fields": fields,
            "footer": {"text": "TradingView → Server Store → Discord | Gold Sniper"},
            "timestamp": now_iso(),
        }]
    }


def send_discord(signal: Dict[str, Any], bookmap: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not DISCORD_WEBHOOK_URL:
        return {"ok": False, "error": "DISCORD_WEBHOOK_URL not set"}
    body = build_discord_embed(signal, bookmap)
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=body, timeout=REQUEST_TIMEOUT_SEC)
        return {"ok": 200 <= r.status_code < 300, "status_code": r.status_code, "text": r.text[:500]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/")
def index():
    return jsonify({
        "ok": True,
        "name": "Gold Sniper Webhook Store Bot",
        "routes": {
            "bookmap_store": "/webhook/bookmap?key=YOUR_KEY",
            "trade_signal": "/webhook/signal?key=YOUR_KEY",
            "status": "/status?key=YOUR_KEY",
            "test_discord": "/test/discord?key=YOUR_KEY"
        }
    })


@app.get("/health")
def health():
    return jsonify({"ok": True, "ts": now_iso()})


@app.post("/webhook/bookmap")
def webhook_bookmap():
    payload = get_payload()
    if not auth_ok(payload):
        return jsonify({"ok": False, "status": "UNAUTHORIZED"}), 401
    event = normalize_event(payload, "BOOKMAP")
    with _lock:
        store = load_store()
        store["bookmap_latest"] = event
        store["history"].append({"kind": "bookmap", "event": event})
        store["history"] = store["history"][-MAX_HISTORY:]
        save_store(store)
    return jsonify({"ok": True, "stored": True, "bookmap_latest": event})


@app.post("/webhook/signal")
def webhook_signal():
    payload = get_payload()
    if not auth_ok(payload):
        return jsonify({"ok": False, "status": "UNAUTHORIZED"}), 401
    signal = normalize_event(payload, "TRADE_SIGNAL")
    with _lock:
        store = load_store()
        bookmap = store.get("bookmap_latest")
        discord_result = send_discord(signal, bookmap)
        store["signal_latest"] = signal
        store["discord_latest"] = discord_result
        store["history"].append({"kind": "signal", "event": signal, "bookmap_used": bookmap, "discord": discord_result})
        store["history"] = store["history"][-MAX_HISTORY:]
        save_store(store)
    return jsonify({"ok": True, "sent_discord": discord_result, "signal": signal, "bookmap_used": bookmap})


@app.post("/webhook")
def webhook_auto():
    """Auto route: if payload type contains BOOKMAP/ORDERFLOW it stores, otherwise sends as signal."""
    payload = get_payload()
    if not auth_ok(payload):
        return jsonify({"ok": False, "status": "UNAUTHORIZED"}), 401
    t = str(payload.get("type", "") or payload.get("source", "") or payload.get("flow", "")).upper()
    if "BOOKMAP" in t or "ORDERFLOW" in t or "FLOW" in t:
        with app.test_request_context('/webhook/bookmap', method='POST', json=payload, query_string=request.query_string):
            return webhook_bookmap()
    with app.test_request_context('/webhook/signal', method='POST', json=payload, query_string=request.query_string):
        return webhook_signal()


@app.get("/status")
def status():
    if not auth_ok({}):
        return jsonify({"ok": False, "status": "UNAUTHORIZED"}), 401
    store = load_store()
    return jsonify({
        "ok": True,
        "bookmap_latest": store.get("bookmap_latest"),
        "signal_latest": store.get("signal_latest"),
        "discord_latest": store.get("discord_latest"),
        "bookmap_age": age_text(store.get("bookmap_latest")),
        "history_count": len(store.get("history", [])),
    })


@app.post("/test/discord")
def test_discord():
    if not auth_ok(get_payload()):
        return jsonify({"ok": False, "status": "UNAUTHORIZED"}), 401
    signal = normalize_event({"signal": "BUY", "symbol": "XAUUSD", "entry": 2350.50, "sl": 2345.0, "tp1": 2355.0, "tp2": 2362.0, "tp3": 2370.0, "signal_id": "TEST_BUY"}, "TRADE_SIGNAL")
    bookmap = normalize_event({"signal": "BUY", "type": "BOOKMAP_ORDERFLOW", "tf": "H1", "price": 2350.40, "score": "BUY", "heatmap": "BUY FLOW"}, "BOOKMAP")
    result = send_discord(signal, bookmap)
    return jsonify({"ok": result.get("ok", False), "discord": result})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
