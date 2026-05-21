# Pinnacle Calendar Reminder App

A modern Flask-based Calendar & Reminder web application that allows users to:

- View calendar dates across years and months
- Create reminders using date or time modes
- Receive automated email reminders
- Manage reminders with full CRUD functionality
- Track reminder history and delivery status
- Receive browser/system notifications

Built using Python, Flask, SQLite, Bootstrap, and JavaScript.

---

# Features

## Calendar System

- Navigate through years and months
- Responsive calendar interface
- Dark modern UI
- Date-based reminder creation
- Same-day time reminder support

---

# Reminder System

## Create Reminders

Users can:
- Set reminder title
- Select date
- Select optional time
- Enter email address

Supports:
- Date reminders
- Same-day time reminders

---

# Reminder History

Displays:
- Reminder title
- Reminder type
- Date
- Time
- Email
- Status

Statuses:
- Pending
- Sent

---

# Edit Reminder

Users can:
- Modify title
- Modify date
- Modify time
- Modify email

Edited reminders replace the existing reminder instead of creating duplicates.

---

# Delete Reminder

Users can:
- Delete reminders permanently
- Confirm deletion using popup dialog

Deleted reminders are removed from:
- UI
- SQLite database
- Scheduler tracking

---

# Email Reminder System

Automated email reminders are sent using:
- Flask-Mail
- Gmail SMTP

Reminder emails trigger automatically based on scheduled reminder time.

---

# Browser Notifications

Supports browser notification permissions using:
- JavaScript Notification API

Users receive desktop/browser reminder alerts.

---

# Tech Stack

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

---

## Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Mail
- APScheduler

---

## Database

- SQLite

---

# Installation

## Clone Repository

```bash
git clone https://github.com/DhruvPatel0110/PythonDev-PinnacleLabs.git
```

## Navigate To Project

```bash
cd PythonDev-PinnacleLabs/Calendar-Reminder
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python app.py
```

---

# Gmail SMTP Setup

Create a `.env` file:

```env
MAIL_USERNAME=yourgmail@gmail.com
MAIL_PASSWORD=your_16_character_app_password
SECRET_KEY=your_secret_key
```

Enable:
- Google 2-Step Verification
- Generate App Password from:
https://myaccount.google.com/apppasswords

---

# Core Functionalities

|       Feature         |Status|
|-----------------------|-----|
| Calendar Navigation   | ✅ |
| Reminder Creation     | ✅ |
| Reminder Editing      | ✅ |
| Reminder Deletion     | ✅ |
| SQLite Database       | ✅ |
| Email Notifications   | ✅ |
| Browser Notifications | ✅ |
| Reminder History      | ✅ |
| Scheduler Automation  | ✅ |

---

# Future Improvements

- Google Calendar sync
- Recurring reminders
- Telegram notifications
- SMS integration
- Dark/Light themes
- User authentication
- Mobile optimization

---

# Learning Outcomes

This project demonstrates:

- Flask backend development
- CRUD operations
- SQLite integration
- Email automation
- Scheduler systems
- Frontend/backend communication
- JavaScript DOM handling
- Real-world reminder workflow

---

# Author

**Dhruv Patel**

GitHub:
https://github.com/DhruvPatel0110

---

# License

This project is for educational and portfolio purposes.