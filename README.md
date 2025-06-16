# 📅 IIITH Calendar Scheduler  
**Lazy? Get your IIIT course info and daily timetable on your calendar in one click!**

Preview at - ```https://siddharthmago.github.io/Skedulr/```

<br>

## 🚀 Overview  
This project automates the process of syncing IIIT-Hyderabad students’ academic schedules with Google Calendar.  
It parses course details and schedules, formats them into calendar events, and integrates them directly into a user’s Google Calendar — making it easy to stay organized without manually entering each event.

<br>

## 🔧 Features

- 📘 Fetches course and timetable data from IIITH student systems  
- 📅 Schedules daily recurring events in your Google Calendar  
- 🕒 Handles start times, durations, and recurrence logic  
- 🔐 Uses secure Google OAuth2 authentication  
- 💻 Clean interface for simplified inputs  
- ✅ One-click setup for students tired of manual calendar entry

<br>

## 📥 Prerequisites

- Python 3.x  
- `pip` (Python package manager)  
- Google account with Calendar access  
- Enabled Google Calendar API via Google Cloud Console

<br>

## 🛠️ Setup Instructions

### 🔐 Step 1: Set up Google Calendar API credentials

Follow these steps:

1. Visit [Google Cloud Console](https://console.cloud.google.com/)  
2. Create or open an existing project  
3. Enable **Google Calendar API**  
4. Create **OAuth 2.0 Client ID** credentials  
5. Download the `credentials.json` file  
6. Save it in the project directory (same folder as your Python scripts)

> 📝 A sample credentials file (`credentials_sample.json`) is included for reference.

<br>

## ▶️ How to Run

Use the provided Makefile for quick setup:

```bash
make install   # Installs required dependencies
make run       # Launches the scheduler
make clean     # Cleans up temporary files
```

Alternatively, you can run the script manually:

```bash
pip install -r requirements.txt
python3 schedulerAPI.py
```

<br>

## 📂 File Structure

```
.
├── schedulerAPI.py        # Core scheduling logic and event formatting
├── googleCal.py           # Google Calendar API interaction layer
├── main.html              # Frontend UI for student inputs
├── credentials.json       # OAuth2 credentials (user-generated)
├── credentials_sample.json# Sample for reference
├── Makefile               # Simplified install/run/clean commands
└── README.md              # You're reading it!
```

<br>

## 💡 Example Use Case

Imagine you’re an IIITH student with 5+ classes a day and recurring labs and tutorials. Rather than manually inputting each class into your calendar:

- Run this script once  
- Authenticate via your Google account  
- Boom! Your semester schedule is in your calendar — synced and color-coded

<br>

## 🛡️ Security Notes

- OAuth flow is handled securely through Google’s recommended libraries  
- No credentials or tokens are shared outside your machine  
- All data remains local unless explicitly pushed to Google Calendar

<br>

## 🙋 FAQ

**Q: Is this tool only for IIITH students?**  
A: Yes, it’s built specifically for IIIT-H timetable structures, though it can be adapted for others.

**Q: Will I need to run it again every day?**  
A: No — recurring events are set up once. Just update if your schedule changes.

**Q: Can I remove all events?**  
A: Yes, you can use the Google Calendar interface to bulk-delete by source/calendar.

<br>

## 🤝 Contributing

Feel free to fork the repo, report issues, or suggest features.  
Pull requests are welcome — just make sure your code is readable and documented!

<br>

## 👨‍💻 Author

Siddharth Mago
Made with ❤️ for IIITH students  
Contributions and bug reports are always appreciated!

---