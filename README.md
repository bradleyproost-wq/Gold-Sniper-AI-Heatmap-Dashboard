# Gold Sniper AI Heatmap Dashboard

Dashboard หน้าตา Bookmap-style สำหรับ Gold Sniper:
- XAUUSD Heatmap
- AI BUY/SELL/WAIT score
- Order Book / DOM
- Liquidity map
- Fake breakout filter
- API endpoint สำหรับ EA / Server

## Run local

```bash
pip install -r requirements.txt
python app.py
```

เปิด:
```text
http://127.0.0.1:5000
```

## Railway

Deploy ได้เลย:
- Start command ใช้ Procfile
- PORT ใช้ของ Railway อัตโนมัติ

## API

### GET /api/state
ดึงข้อมูล dashboard

### POST /api/market
ส่งข้อมูลจริงจาก server/orderflow เข้ามา

ตัวอย่าง:
```json
{
  "symbol": "XAUUSD",
  "price": 2467.48,
  "signal": "BUY",
  "score": 85,
  "fake_breakout": false,
  "heatmap": "BUY_LIQUIDITY"
}
```

### POST /webhook
รับ signal จาก TradingView / server
