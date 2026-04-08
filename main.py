import os
import smtplib
from email.mime.text import MIMEText
import requests

# جيميل
msg = MIMEText("اختبار إرسال من GitHub Actions")
msg["Subject"] = "اختبار"
msg["From"] = os.getenv("EMAIL_USER")
msg["To"] = os.getenv("EMAIL_USER")

with smtplib.SMTP(os.getenv("EMAIL_SMTP_SERVER"), int(os.getenv("EMAIL_SMTP_PORT"))) as server:
    server.starttls()
    server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
    server.send_message(msg)

print("✅ Email sent")

# تلجرام
telegram_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
payload = {"chat_id": os.getenv("TELEGRAM_CHAT_ID"), "text": "اختبار إرسال للتلجرام"}
r = requests.post(telegram_url, data=payload)
print("✅ Telegram sent", r.text)