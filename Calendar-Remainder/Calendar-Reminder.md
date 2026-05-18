# Calendar & Reminder System
## Smart Reminder Scheduler with Email & Browser Notifications

---

# Project Overview

This project is a Python-based Calendar & Reminder application that allows users to:

- View all years, months, dates, and days
- Navigate between past and future dates
- Create reminders using either:
  - Date-based reminders
  - Same-day time-based reminders
- Receive:
  - Email reminders
  - Browser/System notifications

The project focuses on:
- Simplicity
- Real-world usability
- Reminder automation
- Clean UI/UX

---

# Core Features

---

# 1. Full Calendar Navigation

Users should be able to:

- View all years
- Navigate through:
  - Past years
  - Current year
  - Future years
- View:
  - Months
  - Dates
  - Days

---

## Calendar Includes

- Day View
- Month View
- Year View

---

## Example

```plaintext
Monday - 18 May 2026
```

---

# 2. "Remind Me" Button

Every selected date or time section contains a:

```plaintext
Remind Me
```

button.

---

# Reminder Types

When user clicks:

```plaintext
Remind Me
```

they are shown two options:

---

## Option 1 -> Date Reminder

This reminder is for future dates.

---

## User Inputs

### Mandatory
- Reminder Title
- Reminder Date
- Email Address

---

## Optional
- Reminder Time

---

# Reminder Time Logic

## If User Specifies Time

Example:
```plaintext
2026-05-20
18:30
```

The system will:
- Send email at 18:30
- Trigger browser/system notification at 18:30

---

## If User DOES NOT Specify Time

Default values are used.

---

# Default Time Rules

## Email Reminder Default Time
```plaintext
00:01
```

---

## Browser/System Notification Default Time
```plaintext
12:00
```

---

# IMPORTANT NOTE

## All time formats must use:
```plaintext
24-Hour Time Format
```

Examples:
```plaintext
00:01
13:45
18:30
23:59
```

---

# Example Workflow

```plaintext
User selects:
25 May 2026

Reminder Title:
Project Submission

No time entered
```

---

## System Automatically Uses

### Email Reminder Time
```plaintext
00:01
```

### Browser Notification Time
```plaintext
12:00
```

---

# 3. Same-Day Time Reminder

If user selects:

```plaintext
Time Reminder
```

then the reminder applies ONLY for the current day.

---

# User Inputs

- Reminder Title
- Time
- Email Address

---

# Example

```plaintext
Reminder:
Attend Meeting

Time:
18:00
```

---

# System Actions

At 18:00:
- Browser notification appears
- Reminder email is sent

---

# Notification System

---

# 1. Browser/System Notifications

Uses browser notification permission.

---

## Browser Popup

```plaintext
Allow Notifications?
```

If accepted:
- Reminder popup appears on laptop/desktop
- Works even when browser tab is minimized

---

## Example Notification

```plaintext
Reminder
Attend Meeting at 18:00
```

---

# 2. Email Reminder System

Reminder emails are automatically sent using Python backend.

---

## Example Email

```plaintext
Subject: Reminder Notification

Reminder:
Project Submission

Scheduled Time:
18:30
```

---

# Recommended Tech Stack

---

# Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

---

# Backend

- Python
- Flask Framework

---

# Database

## Recommended
- SQLite

Used to store:
- Reminder title
- Reminder date
- Reminder time
- Email address
- Notification status

---

# Required Python Libraries

---

## Flask Libraries

```bash
pip install flask
pip install flask_sqlalchemy
```

---

## Email System

```bash
pip install flask-mail
```

---

## Reminder Scheduler

```bash
pip install apscheduler
```

---

# Suggested Database Tables

---

# Reminders Table

Stores:
- Reminder ID
- Reminder Title
- Reminder Type
- Reminder Date
- Reminder Time
- Email Address
- Notification Status

---

# Users Table (Optional)

Stores:
- User ID
- Username
- Email
- Password

---

# Suggested Folder Structure

```plaintext
calendar-reminder/
│
├── app.py
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── notifications/
│
├── database/
├── reminders/
└── utils/
```

---

# Suggested Website Pages

---

# Pages

- Home Page
- Calendar Dashboard
- Reminder Creation Page
- Reminder History Page
- Settings Page

---

# Reminder Scheduling Logic

---

# Workflow

```plaintext
User creates reminder
        ↓
Reminder stored in SQLite
        ↓
APScheduler continuously checks time
        ↓
If reminder time matches:
    → Send Email
    → Trigger Browser Notification
```

---

# UI Design Suggestions

---

# Theme Style

Modern minimal productivity dashboard.

---

# Suggested Colors

- White
- Light Gray
- Blue
- Dark Navy

---

# UI Features

- Smooth transitions
- Hover effects
- Responsive calendar cards
- Clean reminder popup modal

---

# Additional Features (Optional)

Possible upgrades:
- Dark Mode
- Repeat Reminders
- Weekly Reminder System
- Sound Notification
- Priority Levels
- Reminder Categories

---

# Security Features

- Email validation
- Input sanitization
- Session management
- Notification permission handling

---

# Final Goal

Build a clean and functional Calendar & Reminder application that allows users to:

- Navigate through all dates and years
- Create date/time reminders
- Receive automated email alerts
- Receive browser/system notifications

The project should demonstrate:
- Backend scheduling
- Email automation
- Browser notifications
- Calendar handling
- Database management
- Real-world reminder workflows

---

# Skills Demonstrated Through This Project

- Flask Development
- Database Handling
- Reminder Scheduling
- Email Automation
- Notification Systems
- Frontend UI Design
- Time & Date Processing
- CRUD Operations