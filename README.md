# 🛡️ Acronis Agent Version Watcher

A lightweight Python script that monitors the Acronis Cyber Protect Agent repository for newly published versions and automatically alerts the team via email and Discord — no manual checks required.

---

## 🧩 Problem Statement

In environments managing large numbers of Acronis-protected tenants, keeping track of agent version updates is critical. Outdated agents can introduce security gaps, compatibility issues, and compliance risks.

Previously, this required manually checking for new agent versions on a regular basis — a repetitive task that was easy to forget and inconsistent across a large tenant base.

This script automates the entire process, running continuously and alerting the team the moment a new version is detected.

---

## ✅ Solution Overview

A Python-based monitoring script that scans the Acronis agent repository via HTTP, compares detected versions against a local log, and fires alerts through both email and Discord webhook when a change is found.

- 🔍 Automatically scans the Acronis agent directory
- 🔔 Alerts via Email and Discord webhook
- 🗂️ Persists detected versions to avoid duplicate alerts
- 📋 Logs all activity and errors for auditability
- 🏭 Used in production across 50+ managed tenants

---

## 🛠️ Tech Stack

- **Python 3.x**
- `requests` — HTTP scanning
- `bs4` (BeautifulSoup) — HTML parsing
- `smtplib` — Email delivery via SMTP
- **Discord Webhook** — Team notifications

---

## ⚙️ How It Works

1. The script fetches the Acronis agent directory page via HTTP
2. It parses the page to extract all currently available agent versions
3. Detected versions are compared against `detected_versions.json`
4. If a new version is found, alerts are sent via email and Discord
5. The new version is saved to `detected_versions.json` to prevent duplicate alerts
6. All activity and errors are logged to `alert_log.txt`

---

## 📌 Example Alert

```
Subject: Acronis Cyber Protect Agent Update

A new version of the Acronis Cyber Protect Agent has been detected.

Current versions:
- 25.3.39872
- 25.4.40030

Change detected:
25.3.39872 ➝ 25.4.40030
```

---

## 🚀 How to Deploy

**1. Clone the repository**
```bash
git clone https://github.com/steliosvardakas/acronis-agent-watcher
cd acronis-agent-watcher
```

**2. Install dependencies**
```bash
pip install requests beautifulsoup4
```

**3. Configure credentials**
Open `watcher.py` and update the following variables:
- SMTP server, email address, and password
- Discord webhook URL
- Acronis agent directory URL

**4. Run the script**
```bash
python watcher.py
```

For continuous monitoring, run it as a scheduled task (Windows Task Scheduler) or a cron job (Linux).

---

## 📁 Repository Structure

```
acronis-agent-watcher/
├── watcher.py                  # Main monitoring script
├── detected_versions.json      # Persisted version log
├── alert_log.txt               # Activity and error log
└── README.md
```

---

## 🔮 Future Improvements

- [ ] `.env` support for secure credential management
- [ ] Improved logging using Python's `logging` module
- [ ] CLI options (`--once`, `--verbose`, `--dry-run`)
- [ ] Support for multiple Acronis regions
- [ ] Configurable check interval

---

## 👤 Author

**Stylianos Vardakas**  
Cyber Security Support Engineer  
[LinkedIn](https://www.linkedin.com/in/stylianos-vardakas/) • [GitHub](https://github.com/steliosvardakas)

*Implemented and used in production at a managed cybersecurity services provider.*

---

## 📄 License

[MIT](LICENSE)
