from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

STATE = {
    "symbol": "XAUUSD",
    "price": 4537.80,
    "signal": "BUY",
    "score": 85,
    "confidence": 87,
    "market_bias": "BULLISH",
    "volatility": "HIGH",
    "spread": 0.28,
    "latency_ms": 18,
    "server": "Singapore (SG)",
    "delta": 2845,
    "imbalance": 65,
    "buy_wall": "4536.90",
    "sell_wall": "4538.50",
    "sweep_zone": "4537.10 - 4537.30",
    "fake_breakout": False,
    "reason": [
        "Liquidity sweep detected",
        "Strong delta buying",
        "Orderflow bullish",
        "AI confidence high"
    ],
    "candles": [],
    "heatmap_levels": [],
    "orderbook": {
        "asks": [],
        "bids": []
    },
    "trades": []
}


def build_market():
    base = STATE["price"]

    candles = []
    p = base

    for _ in range(60):
        o = round(p + random.uniform(-1, 1), 2)
        c = round(o + random.uniform(-1.5, 1.5), 2)
        h = round(max(o, c) + random.uniform(0, 1), 2)
        l = round(min(o, c) - random.uniform(0, 1), 2)
        v = random.randint(10, 80)

        candles.append({
            "o": o,
            "h": h,
            "l": l,
            "c": c,
            "v": v
        })

        p = c

    STATE["candles"] = candles

    STATE["heatmap_levels"] = [
        {
            "price": round(base + random.uniform(-5, 5), 2),
            "strength": random.randint(20, 100)
        }
        for _ in range(12)
    ]

    STATE["orderbook"] = {
        "asks": [
            {
                "price": round(base + i * 0.1, 2),
                "size": random.randint(5, 50)
            }
            for i in range(1, 8)
        ],
        "bids": [
            {
                "price": round(base - i * 0.1, 2),
                "size": random.randint(5, 50)
            }
            for i in range(1, 8)
        ]
    }

    STATE["trades"] = [
        {
            "time": time.strftime("%H:%M:%S"),
            "price": round(base + random.uniform(-1, 1), 2),
            "size": round(random.uniform(0.1, 5), 2),
            "side": random.choice(["Buy", "Sell"])
        }
        for _ in range(12)
    ]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "ok": True,
        "status": "online"
    })


@app.route("/api/state")
def api_state():
    build_market()
    return jsonify(STATE)


@app.route("/api/market", methods=["POST"])
def api_market():
    data = request.json

    if not data:
        return jsonify({
            "ok": False,
            "error": "missing json"
        }), 400

    STATE.update(data)

    return jsonify({
        "ok": True,
        "updated": True
    })


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return jsonify({
            "ok": False,
            "error": "missing payload"
        }), 400

    signal = data.get("signal", "WAIT")

    STATE["signal"] = signal
    STATE["score"] = data.get("score", 50)
    STATE["confidence"] = data.get("confidence", 50)
    STATE["market_bias"] = "BULLISH" if signal == "BUY" else "BEARISH"

    return jsonify({
        "ok": True,
        "signal": signal
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
