# 🛡️ Acronis Agent Version Watcher (v1.0)

This script monitors the Acronis Cyber Protect Agent repository and alerts the team via email and Discord when new agent versions are detected.

---

## 🚀 Features

- Automatically scans Acronis agent directories (via HTTP)
- Detects newly published versions
- Sends alerts via:
  - 📧 Email
  - 🔔 Discord (Webhook)
- Keeps a log of previously detected versions (`detected_versions.json`)
- Records all activity and errors in `alert_log.txt`

---

## 🛠️ Tech Stack

- Python 3.x
- `requests`, `bs4`, `smtplib`
- Discord webhook integration
- Email SMTP via Gmail

---

## 📌 Example Email

```
Subject: Acronis Cyber Protect Agent Update

A new version of the Acronis Cyber Protect Agent has been detected.

Current versions:
- 25.3.39872
- 25.4.40030

Change detected:
25.3.39872 ➝ 25.4.40030

View: https://eu8-cloud.acronis.com/download/u/baas/4.0/
```

---

## 🧠 Purpose

Used in real-world production to manage 50+ tenants and keep track of agent versioning, without relying on manual checks. Saves time and ensures systems stay up-to-date.

---

## 👤 Author

**Stylianos Vardakas**  
_Built with ChatGPT support, implemented & used in production._

---

## 🏷️ Version

**v1.0** – First public version  
➡️ Future versions will include:
- `.env` support for secure credentials
- Better logging with `logging` module
- CLI options (`--once`, `--verbose`, etc.)
