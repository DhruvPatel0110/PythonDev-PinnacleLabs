# Calendar & Reminder System - Complete Setup Instructions

This document provides detailed step-by-step instructions to run the Calendar & Reminder app successfully in GitHub Codespaces or locally.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Clone and Setup](#clone-and-setup)
3. [Install Dependencies](#install-dependencies)
4. [Configure Gmail SMTP](#configure-gmail-smtp)
5. [Environment Variables Setup](#environment-variables-setup)
6. [Database Initialization](#database-initialization)
7. [Run the Application](#run-the-application)
8. [Access the App](#access-the-app)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### For GitHub Codespaces
- GitHub account
- Repository forked/cloned to your account
- No additional software needed (Python, Git, etc. pre-installed)

### For Local Development
- Python 3.8 or higher
- Git installed
- pip (Python package manager)
- A Gmail account (for email notifications)

---

## Clone and Setup

### Step 1: Open Repository in GitHub Codespaces
1. Go to your forked repository on GitHub
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for the environment to load (2-3 minutes)

### Step 2: Navigate to Project Directory
```bash
cd /workspaces/PythonDev-PinnacleLabs/Calendar-Remainder
```

---

## Install Dependencies

### Step 3: Install Required Python Libraries
All dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

### What Gets Installed:
- **Flask** — Web framework
- **Flask-SQLAlchemy** — Database ORM
- **Flask-Mail** — Email sending
- **APScheduler** — Reminder scheduling
- **python-dotenv** — Environment variable management

### Verification
To verify installation:
```bash
pip list
```
You should see all five packages listed.

---

## Configure Gmail SMTP

This app sends reminders via Gmail. Follow these steps to set up Gmail:

### Step 4: Enable 2-Factor Authentication (Gmail)
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** (left sidebar)
3. Scroll to **How you sign in to Google**
4. Enable **2-Step Verification** (if not already enabled)

### Step 5: Generate App Password
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select **Mail** and **Windows Computer** (or your device type)
3. Click **Generate**
4. Copy the 16-character password shown
5. **Keep this password secure** — you'll need it in the next step

### Example App Password:
```
abcd efgh ijkl mnop
```
(Remove spaces when pasting into .env)

---

## Environment Variables Setup

### Step 6: Create `.env` File
The `.env` file stores sensitive credentials. It's already listed in `.gitignore`, so it won't be committed.

1. Open the `.env` file in `Calendar-Remainder/` directory:
   ```bash
   nano .env
   ```

2. Add the following variables:
   ```env
   MAIL_USERNAME=your_gmail@gmail.com
   MAIL_PASSWORD=abcdefghijklmnop
   SECRET_KEY=your-random-secret-key-here-make-it-unique
   ```

3. Replace the values:
   - `MAIL_USERNAME`: Your Gmail address (e.g., `user@gmail.com`)
   - `MAIL_PASSWORD`: The 16-character app password from Step 5 (without spaces)
   - `SECRET_KEY`: Any random string (minimum 16 characters for security)

### Example .env:
```env
MAIL_USERNAME=myemail@gmail.com
MAIL_PASSWORD=abcdefghijklmnop
SECRET_KEY=my_super_secret_key_1234567890
```

4. Save the file (press `Ctrl+O`, then `Enter`, then `Ctrl+X` to exit nano)

5. Verify the file was created:
   ```bash
   cat .env
   ```

---

## Database Initialization

### Step 7: Initialize SQLite Database
The database will be created automatically when the Flask app starts. However, you can pre-initialize it:

```bash
python app.py
```

When the app runs, it will create `database/reminders.db` if it doesn't exist.

---

## Run the Application

### Step 8: Start the Flask App
From the `Calendar-Remainder` directory, run:

```bash
python app.py
```

### Expected Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * WARNING: This is a development server. Do not use it in production.
 * Running on http://127.0.0.1:5000
```

---

## Access the App

### Step 9: Open in Browser
**In GitHub Codespaces:**
1. A notification will appear: **"Your application running on port 5000 is available"**
2. Click **Open in Browser** or manually navigate to the forwarded URL
3. The calendar UI should load

**Locally:**
- Open your browser and go to `http://localhost:5000`

---

## Features to Test

### Step 10: Test the App
1. **Calendar Navigation:**
   - Click **Prev/Next Year** and **Prev/Next Month** buttons
   - Select a date to view the day

2. **Browser Notifications:**
   - A permission dialog will appear asking to show notifications
   - Click **Allow** to enable notifications

3. **Create a Reminder:**
   - Click **Remind Me** button on a selected date
   - Choose **Date Reminder** or **Same-Day Time Reminder**
   - Fill in the form:
     - **Reminder Title**: e.g., "Project Submission"
     - **Date**: Select future date
     - **Time**: Enter time in 24-hour format (e.g., 18:30)
     - **Email**: Your email address
   - Click **Set Date Reminder** or **Set Time Reminder**

4. **Check Reminder History:**
   - Open browser console (F12)
   - Navigate to `/reminder_history` endpoint to see all saved reminders

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Ensure all libraries are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Error: MAIL_USERNAME or MAIL_PASSWORD not set"
**Solution:** Check that `.env` file exists and contains correct variables:
```bash
cat .env
```
Verify `MAIL_USERNAME` and `MAIL_PASSWORD` are set correctly.

### Issue: "Gmail says 'Less secure app access denied'"
**Solution:** You must use an **App Password**, not your regular Gmail password. Follow Step 5 again to generate an app-specific password.

### Issue: "Port 5000 already in use"
**Solution:** Either:
- Stop the previous Flask process: `pkill -f "python app.py"`
- Run on a different port: `python -c "app.run(port=5001)"`

### Issue: "Database file not created"
**Solution:** Manually trigger database creation:
```bash
python
from app import app, db
with app.app_context():
    db.create_all()
exit()
```

### Issue: "Notification permission denied"
**Solution:** 
- Reload the page (F5)
- Click **Allow** when the permission dialog appears
- Or check browser notification settings

### Issue: "Email not sending"
**Solution:**
1. Verify `.env` credentials are correct
2. Check the Flask console for error messages
3. Ensure Gmail 2FA and App Password are set up (Step 4-5)
4. Disable any VPN/proxy that might block SMTP

---

## File Structure Reference

```
Calendar-Remainder/
├── app.py                          # Main Flask app
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (keep secret!)
├── .gitignore                      # Git ignore file
├── instructions.md                 # This file
├── deletets.md                     # List of unnecessary files
├── templates/
│   └── calendar.html               # Calendar UI
├── static/
│   ├── css/
│   │   └── calendar.css            # Calendar styles
│   ├── js/
│   │   └── calendar.js             # Calendar logic
│   └── notifications/
│       └── notify.js               # Browser notification system
├── database/                       # SQLite DB location
├── reminders/                      # Reminder logic (future)
└── utils/                          # Utility functions (future)
```

---

## Security Checklist

Before deploying:
- [ ] `.env` is in `.gitignore` (already configured)
- [ ] Gmail App Password is used (not regular password)
- [ ] `SECRET_KEY` in `.env` is unique and random
- [ ] Database file (`reminders.db`) is not committed to Git
- [ ] No sensitive data is logged to console

---

## Next Steps

1. **Customize Design:** Edit `static/css/calendar.css`
2. **Add More Routes:** Extend `app.py` with additional endpoints
3. **Deploy:** When ready, deploy to Heroku, AWS, or another platform
4. **Add User Authentication:** Implement login/registration for multiple users

---

## Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review Flask and SQLAlchemy documentation
3. Check Gmail SMTP configuration
4. Review the `Calendar-Reminder.md` specification file

---

**Setup Complete! Happy reminding! 🎉**
