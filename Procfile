from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import time, random, math, os

app = Flask(__name__)
CORS(app)

STATE = {
    "symbol": "XAUUSD",
    "timeframe": "M1",
    "price": 2467.48,
    "signal": "BUY",
    "score": 85,
    "confidence": 85,
    "market_bias": "BULLISH",
    "volatility": "MEDIUM",
    "spread": 0.28,
    "fake_breakout": False,
    "server": "Singapore (SG)",
    "latency_ms": 18,
    "heatmap": "BUY_LIQUIDITY",
    "reason": [
        "Liquidity Buy Wall",
        "Bullish Imbalance",
        "Sweep Liquidity",
        "Trend Alignment (H1)"
    ],
    "updated": int(time.time())
}

def make_candles(n=85, base=2465.0):
    out = []
    price = base
    for i in range(n):
        drift = math.sin(i / 9) * 0.25 + random.uniform(-0.24, 0.32)
        o = price
        c = price + drift
        h = max(o, c) + random.uniform(0.05, 0.55)
        l = min(o, c) - random.uniform(0.05, 0.55)
        price = c
        out.append({
            "t": i,
            "o": round(o, 2),
            "h": round(h, 2),
            "l": round(l, 2),
            "c": round(c, 2),
            "v": random.randint(20, 180)
        })
    # last candles align with state price
    diff = STATE["price"] - out[-1]["c"]
    for x in out:
        for k in ["o","h","l","c"]:
            x[k] = round(x[k] + diff, 2)
    return out

def make_heatmap():
    levels = []
    price = STATE["price"]
    for i in range(-18, 19):
        p = round(price + i * 0.12, 2)
        dist = abs(i)
        strength = max(5, 100 - dist * 5 + random.randint(-15, 25))
        if i in [-10, -9, -8, -7, 6, 7, 8]:
            strength += 80
        side = "buy" if i < 0 else "sell"
        levels.append({"price": p, "strength": min(100, strength), "side": side})
    return levels

def make_orderbook():
    price = STATE["price"]
    asks, bids = [], []
    for i in range(1, 11):
        asks.append({"price": round(price + i * 0.05, 2), "size": round(random.uniform(18, 95), 1)})
        bids.append({"price": round(price - i * 0.05, 2), "size": round(random.uniform(22, 110), 1)})
    return {"asks": asks[::-1], "bids": bids}

def make_trades():
    trades = []
    price = STATE["price"]
    for i in range(18):
        side = "Buy" if random.random() > 0.43 else "Sell"
        trades.append({
            "time": time.strftime("%H:%M:%S", time.localtime(time.time()-i)),
            "price": round(price + random.uniform(-0.25,0.25), 2),
            "size": round(random.uniform(0.2, 2.8), 2),
            "side": side
        })
    return trades

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"ok": True, "status": "ONLINE", "ts": int(time.time())})

@app.route("/api/state")
def api_state():
    STATE["latency_ms"] = random.randint(12, 31)
    STATE["updated"] = int(time.time())
    payload = dict(STATE)
    payload["candles"] = make_candles(base=STATE["price"]-2.8)
    payload["heatmap_levels"] = make_heatmap()
    payload["orderbook"] = make_orderbook()
    payload["trades"] = make_trades()
    payload["delta"] = random.randint(900, 3800)
    payload["imbalance"] = random.randint(45, 76)
    payload["buy_wall"] = f"{STATE['price']-0.78:.2f} - {STATE['price']-0.62:.2f}"
    payload["sell_wall"] = f"{STATE['price']+0.62:.2f} - {STATE['price']+0.78:.2f}"
    payload["sweep_zone"] = f"{STATE['price']-0.88:.2f} - {STATE['price']-0.58:.2f}"
    return jsonify(payload)

@app.route("/api/market", methods=["POST"])
@app.route("/webhook", methods=["POST"])
def update_market():
    data = request.get_json(silent=True) or {}
    for k in ["symbol", "timeframe", "price", "signal", "score", "confidence", "market_bias", "volatility", "spread", "fake_breakout", "heatmap"]:
        if k in data:
            STATE[k] = data[k]
    if "reason" in data and isinstance(data["reason"], list):
        STATE["reason"] = data["reason"]
    STATE["updated"] = int(time.time())
    return jsonify({"ok": True, "state": STATE})

@app.route("/api/ea_signal")
def ea_signal():
    sig = STATE["signal"]
    if STATE.get("fake_breakout") or int(STATE.get("score", 0)) < 70:
        sig = "WAIT"
    return jsonify({
        "ok": True,
        "symbol": STATE["symbol"],
        "signal": sig,
        "score": STATE["score"],
        "heatmap": STATE["heatmap"],
        "fake_breakout": STATE["fake_breakout"],
        "reason": STATE["reason"],
        "signal_id": f"GS_HEATMAP_{STATE['updated']}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
