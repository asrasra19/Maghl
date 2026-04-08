# storage/ibfs.py

import requests
import os
from publishers.drive import GoogleDrivePublisher

def load_jobs_from_ipfs():
    jobs = []
    cids = os.getenv("IPFS_CIDS")

    if cids:
        for cid in cids.split(","):
            url = f"https://ipfs.io/ipfs/{cid.strip()}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    jobs.extend(response.json())
            except Exception as e:
                print(f"⚠️ فشل تحميل من IPFS: {e}")

    # لو فشل IPFS → نجرب Google Drive
    if not jobs:
        jobs = load_jobs_from_google_drive()

    # لو فشل Google Drive → نجرب مصادر أخرى (Telegram, Facebook, WhatsApp)
    if not jobs:
        jobs = load_jobs_from_other_sources()

    return jobs


def load_jobs_from_google_drive():
    jobs = []
    client_id = os.getenv("GOOGLE_DRIVE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_DRIVE_CLIENT_SECRET")
    refresh_token = os.getenv("GOOGLE_DRIVE_REFRESH_TOKEN")

    if client_id and client_secret and refresh_token:
        drive = GoogleDrivePublisher(client_id, client_secret, refresh_token)
        file_id = os.getenv("GOOGLE_DRIVE_FILE_ID")  # ID الملف المخزن في Google Drive
        if file_id:
            data = drive.download_file(file_id)
            if data:
                jobs.extend(data)
    else:
        print("⚠️ Google Drive غير مفعل (Secrets ناقصة)")
    return jobs


def load_jobs_from_other_sources():
    """
    خطة بديلة إضافية: تحميل المهام من روابط خارجية
    مثل ملفات JSON مرفوعة على Facebook أو Telegram أو WhatsApp.
    """
    jobs = []
    urls = os.getenv("BACKUP_URLS")  # مثال: "https://example.com/jobs.json,https://another.com/data.json"
    if urls:
        for url in urls.split(","):
            try:
                response = requests.get(url.strip(), timeout=10)
                if response.status_code == 200:
                    jobs.extend(response.json())
            except Exception as e:
                print(f"⚠️ فشل تحميل من {url}: {e}")
    return jobs