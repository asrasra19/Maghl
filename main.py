# main.py

import os
import json
from flask import Flask, render_template, request, redirect, url_for
from scheduler.jobs import Job, JobManager
from scheduler.modes import unified_system
from publishers.facebook import FacebookPublisher
from publishers.twitter import TwitterPublisher
from publishers.instagram import InstagramPublisher
from publishers.telegram import TelegramPublisher
from publishers.whatsapp import WhatsAppPublisher
from publishers.youtube import YouTubePublisher
from publishers.email import EmailPublisher
from publishers.organizations import OrganizationPublisher

app = Flask(__name__)
job_manager = JobManager()

# تحميل ملف المنظمات
with open("data/organizations.json", "r", encoding="utf-8") as f:
    org_data = json.load(f)
org_publisher = OrganizationPublisher([org["url"] for org in org_data["organizations"]])

# تهيئة الناشرين باستخدام Environment Variables
facebook_pub = FacebookPublisher(os.getenv("FACEBOOK_ACCESS_TOKEN"), "PAGE_ID")
twitter_pub = TwitterPublisher(os.getenv("TWITTER_API_KEY"))
instagram_pub = InstagramPublisher(os.getenv("INSTAGRAM_ACCESS_TOKEN"), "PAGE_ID")
telegram_pub = TelegramPublisher(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))
whatsapp_pub = WhatsAppPublisher(os.getenv("WHATSAPP_TOKEN"), os.getenv("WHATSAPP_PHONE_ID"), os.getenv("RECIPIENT_NUMBER"))
youtube_pub = YouTubePublisher(os.getenv("YOUTUBE_API_KEY"), os.getenv("YOUTUBE_CHANNEL_ID"))
email_pub = EmailPublisher(os.getenv("EMAIL_SMTP_SERVER"), os.getenv("EMAIL_SMTP_PORT"), os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))

publishers = {
    "facebook": facebook_pub,
    "twitter": twitter_pub,
    "instagram": instagram_pub,
    "telegram": telegram_pub,
    "whatsapp": whatsapp_pub,
    "youtube": youtube_pub,
    "email": email_pub,
    "organizations": org_publisher
}

@app.route("/")
def dashboard():
    return render_template("dashboard.html", jobs=job_manager.jobs)

@app.route("/add_job", methods=["POST"])
def add_job():
    text = request.form["text"]
    media = request.form.get("media")
    platform = request.form["platform"]
    local_time = request.form["local_time"]
    tz_id = request.form["tz_id"]

    action = {"text": text}
    if media:
        action["media"] = media

    job = Job(local_time, tz_id, action, publishers.get(platform))
    job_manager.add_job(job)
    return redirect(url_for("dashboard"))

@app.route("/run_jobs")
def run_jobs():
    unified_system(job_manager.jobs)
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)