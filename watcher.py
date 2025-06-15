# This script monitors Acronis Agent versions from the EU8 data center only.
# URL: https://eu8-cloud.acronis.com/download/u/baas/4.0/

import requests
from bs4 import BeautifulSoup
import time
import json
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

# === CONFIGURATION ===
BASE_URL = "https://eu8-cloud.acronis.com/download/u/baas/4.0/"
CHECK_INTERVAL = 3600  # seconds
VERSIONS_FILE = "detected_versions.json"
ALERT_LOG = "alert_log.txt"

# === DISCORD ALERT SETTINGS ===
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/"

# === EMAIL ALERT SETTINGS ===
EMAIL_ENABLED = True
SMTP_SERVER = ""
SMTP_PORT = 587
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
EMAIL_FROM = SMTP_USERNAME
EMAIL_TO = [""]

# === CORE FUNCTIONS ===

def fetch_subdirs():
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Match ANY href that ends with '/'
        subdirs = [
            a['href'].strip('/')
            for a in soup.find_all('a', href=True)
            if a['href'].endswith('/') and not a['href'].startswith('../')
        ]
        return sorted(set(subdirs))

    except Exception as e:
        log_error(f"Fetch failed: {e}")
        return []


def load_previous_versions():
    if not os.path.exists(VERSIONS_FILE):
        return []
    with open(VERSIONS_FILE, 'r') as f:
        try:
            return json.load(f)
        except Exception as e:
            log_error(f"Version file corrupt: {e}")
            return []

def save_versions(versions):
    with open(VERSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(versions, f, indent=2)

def log_error(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] ❌ ERROR: {message}")
    with open(ALERT_LOG, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")

def alert_new_versions(new_versions):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"[{timestamp}] 🚨 New version(s) detected: {', '.join(new_versions)}"
    print(message)
    with open(ALERT_LOG, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def send_discord_version_report(current, new, previous):
    if not DISCORD_WEBHOOK_URL or "your_webhook_here" in DISCORD_WEBHOOK_URL:
        return

    current_sorted = sorted(current)
    previous_sorted = sorted(previous)

    content = "✅ **Current Acronis Versions:**\n"
    content += "\n".join(f"🔹 `{ver}`" for ver in current_sorted)

    if new:
        old_latest = previous_sorted[-1] if previous_sorted else "None"
        new_latest = current_sorted[-1]
        content += "\n\n🔁 **Change detected:**\n"
        content += f"`{old_latest}` ➝ `{new_latest}`"
    else:
        return  # Skip if no change

    content += f"\n🔗 {BASE_URL}"

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
        response.raise_for_status()
    except Exception as e:
        log_error(f"Discord alert failed: {e}")

def send_email_alert(current, new, previous):
    if not EMAIL_ENABLED:
        return

    msg = EmailMessage()
    msg['Subject'] = "Acronis Cyber Protect Agent Update"
    msg['From'] = EMAIL_FROM
    msg['To'] = ", ".join(EMAIL_TO)

    old_latest = previous[-1] if previous else "None"
    new_latest = current[-1]

    body = (
        "A new version of the Acronis Cyber Protect Agent has been detected.\n" +
        "\n" +
        "Current versions:\n" +
        "\n".join(f"- {v}" for v in current) +
        "\n\nChange detected:\n" +
        f"{old_latest} ➝ {new_latest}\n\n" +
        f"View: {BASE_URL}"
    )

    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print("📧 Email alert sent.")
    except Exception as e:
        log_error(f"Email alert failed: {e}")

def check_for_updates():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 Scanning {BASE_URL}")
    current_versions = fetch_subdirs()
    previous_versions = load_previous_versions()
    new_versions = sorted(set(current_versions) - set(previous_versions))

    if new_versions:
        alert_new_versions(new_versions)
        save_versions(current_versions)
        send_discord_version_report(current_versions, new_versions, previous_versions)
        send_email_alert(current_versions, new_versions, previous_versions)

# === MAIN LOOP ===
if __name__ == "__main__":
    print("🛡️ Acronis Watchdog activated. Monitoring for new versions...")
    while True:
        check_for_updates()
        time.sleep(CHECK_INTERVAL)
