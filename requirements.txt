# Gold Sniper AI Heatmap Dashboard - Render Clean Fixed

สำคัญ: อย่าเอา render.yaml ไปใส่ใน requirements.txt

## Render Manual Setting

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app --bind 0.0.0.0:$PORT

## Test URL

/health
/api/state
/webhook
