# Gold Sniper Webhook Store Bot

หน้าที่:
1. รับ Webhook จาก Bookmap/Orderflow แล้วเก็บเป็นข้อมูลล่าสุด
2. รับ Webhook สัญญาซื้อขายจาก Indicator
3. เอา “Bookmap ล่าสุด” + “Signal ใหม่” + “ราคาอ้างอิง” ส่งเข้า Discord เป็น Embed สวยๆ

## Deploy บน Railway
1. สร้าง Project ใหม่
2. Upload โฟลเดอร์/ZIP นี้ หรือ push เข้า GitHub
3. ใส่ Variables:
   - `GS_API_KEY=GOLD_SNIPER_VIP_SN`
   - `DISCORD_WEBHOOK_URL=ลิงก์ Discord Webhook ของคุณ`
   - `STORE_FILE=signal_store.json`
   - `MAX_BOOKMAP_AGE_SEC=86400`
4. Deploy

## URL ที่ใช้ใน TradingView Alert

### 1) Bookmap / Orderflow webhook
ส่งเข้ามาเพื่อ “เก็บล่าสุด”:
```
https://YOUR-RAILWAY-APP.up.railway.app/webhook/bookmap?key=GOLD_SNIPER_VIP_SN
```

ตัวอย่าง message:
```json
{"key":"GOLD_SNIPER_VIP_SN","type":"BOOKMAP_ORDERFLOW","signal":"BUY","symbol":"XAUUSD","tf":"H1","price":2350.40,"score":"BUY","heatmap":"BUY FLOW"}
```

### 2) Trade Signal webhook
ส่งเข้ามาเพื่อ “รวมกับ Bookmap ล่าสุด แล้วส่ง Discord”:
```
https://YOUR-RAILWAY-APP.up.railway.app/webhook/signal?key=GOLD_SNIPER_VIP_SN
```

ตัวอย่าง message:
```json
{"key":"GOLD_SNIPER_VIP_SN","signal":"BUY","side":"BUY","symbol":"XAUUSD","timeframe":"H1","signal_id":"BUY_12345","entry":2351.25,"sl":2345.00,"tp1":2356.00,"tp2":2363.00,"tp3":2375.00}
```

## เช็คสถานะ
```
https://YOUR-RAILWAY-APP.up.railway.app/status?key=GOLD_SNIPER_VIP_SN
```

## ทดสอบ Discord
ใช้ POST:
```
https://YOUR-RAILWAY-APP.up.railway.app/test/discord?key=GOLD_SNIPER_VIP_SN
```

## หมายเหตุสำคัญ
- Bookmap webhook ต้องยิงมาก่อน Signal webhook อย่างน้อย 1 ครั้ง เพื่อให้มีข้อมูลล่าสุดเก็บไว้
- ถ้า Signal มาแต่ยังไม่มี Bookmap ระบบยังส่ง Discord ได้ แต่ช่อง Bookmap จะเป็น `-`
- ราคาอ้างอิงจะใช้ `entry` ของสัญญาก่อน ถ้าไม่มีจะใช้ `price` จาก Signal หรือ Bookmap ล่าสุด
