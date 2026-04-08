# storage/timeapi.py

import requests
from datetime import datetime
import pytz
import time
import sqlite3

# المصدر الرسمي لأسماء المناطق الزمنية:
# https://www.iana.org/time-zones

def save_last_time(tz_id, dt):
    conn = sqlite3.connect("time_backup.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS times (tz TEXT PRIMARY KEY, dt TEXT)")
    c.execute("REPLACE INTO times (tz, dt) VALUES (?, ?)", (tz_id, dt.isoformat()))
    conn.commit()
    conn.close()

def get_last_time(tz_id):
    conn = sqlite3.connect("time_backup.db")
    c = conn.cursor()
    c.execute("SELECT dt FROM times WHERE tz=?", (tz_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return datetime.fromisoformat(row[0])
    return None

def get_current_time(tz_id, retries=3):
    """
    يحاول جلب الوقت الحالي من WorldTimeAPI.
    لو فشل، يستخدم مكتبة pytz مباشرة.
    ولو فشل تمامًا، يرجع آخر وقت محفوظ من SQLite.
    """
    url = f"https://worldtimeapi.org/api/timezone/{tz_id}"

    # المحاولة مع WorldTimeAPI
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                dt = datetime.fromisoformat(data["datetime"])
                save_last_time(tz_id, dt)  # حفظ تلقائي
                return dt
        except Exception as e:
            print(f"⚠️ محاولة {attempt+1} فشلت: {e}")
            time.sleep(2)

    # fallback: استخدام pytz محليًا
    try:
        tz = pytz.timezone(tz_id)
        dt = datetime.now(tz)
        save_last_time(tz_id, dt)  # حفظ تلقائي
        return dt
    except Exception as e:
        print(f"❌ خطأ في pytz: {e}")
        # fallback النهائي: استرجاع آخر وقت محفوظ
        return get_last_time(tz_id)