import os
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from datetime import datetime, date

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
scheduler = BackgroundScheduler()
scheduler.start()

# Import and register blueprints/routes here
# from reminders.routes import reminders_bp
# app.register_blueprint(reminders_bp)

class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    reminder_type = db.Column(db.String(50), nullable=False)
    reminder_date = db.Column(db.Date, nullable=False)
    reminder_time = db.Column(db.Time, nullable=True)
    email = db.Column(db.String(255), nullable=False)
    notification_status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reminder {self.id} - {self.title}>'

@app.route('/')
def home():
    return render_template('calendar.html')

# Add reminder route (POST)
@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    data = request.get_json() if request.is_json else request.form
    title = data.get('title')
    reminder_type = data.get('reminder_type')
    reminder_date = data.get('reminder_date')
    reminder_time = data.get('reminder_time')
    email = data.get('email')
    if not (title and reminder_type and email):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    try:
        reminder = Reminder(
            title=title,
            reminder_type=reminder_type,
            reminder_date=reminder_date,
            reminder_time=reminder_time,
            email=email,
            notification_status='pending'
        )
        db.session.add(reminder)
        db.session.commit()
        send_email_notification(reminder)  # Trigger email immediately (or let scheduler handle)
        return jsonify({'success': True, 'reminder_id': reminder.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Reminder history route
@app.route('/reminder_history', methods=['GET'])
def reminder_history():
    reminders = Reminder.query.order_by(Reminder.created_at.desc()).all()
    result = [
        {
            'id': r.id,
            'title': r.title,
            'reminder_type': r.reminder_type,
            'reminder_date': str(r.reminder_date),
            'reminder_time': r.reminder_time.strftime('%H:%M') if r.reminder_time else None,
            'email': r.email,
            'notification_status': r.notification_status,
            'created_at': r.created_at.isoformat()
        }
        for r in reminders
    ]
    return jsonify(result)

# --- APScheduler Job for Reminders ---
def check_and_trigger_reminders():
    now = datetime.now()
    today = date.today()
    reminders = Reminder.query.filter_by(reminder_date=today, notification_status='pending').all()
    for reminder in reminders:
        # Check if reminder_time is set and matches current time (24-hour format)
        if reminder.reminder_time:
            reminder_time_str = reminder.reminder_time.strftime('%H:%M')
            now_time_str = now.strftime('%H:%M')
            if reminder_time_str == now_time_str:
                send_email_notification(reminder)
                trigger_browser_notification(reminder)
                reminder.notification_status = 'sent'
                db.session.commit()
        else:
            # If no time, use default (00:01 for email, 12:00 for browser)
            if now.strftime('%H:%M') == '00:01':
                send_email_notification(reminder)
                reminder.notification_status = 'sent'
                db.session.commit()
            elif now.strftime('%H:%M') == '12:00':
                trigger_browser_notification(reminder)
                # Don't mark as sent if email not sent yet

# Dummy email notification function

def send_email_notification(reminder):
    subject = "Reminder Notification"
    reminder_time = reminder.reminder_time.strftime('%H:%M') if reminder.reminder_time else 'N/A'
    body = f"""
    Reminder: {reminder.title}
    Scheduled Date: {reminder.reminder_date}
    Scheduled Time: {reminder_time}
    """
    msg = Message(subject=subject, recipients=[reminder.email], body=body)
    try:
        mail.send(msg)
        print(f"[EMAIL SENT] To: {reminder.email} | Title: {reminder.title} | Date: {reminder.reminder_date} | Time: {reminder_time}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

# Dummy browser notification event trigger

def trigger_browser_notification(reminder):
    # In production, use WebSocket or server-sent events to notify browser
    print(f"[BROWSER] Reminder: {reminder.title} at {reminder.reminder_time}")

# Schedule the job to run every minute
scheduler.add_job(func=check_and_trigger_reminders, trigger='interval', seconds=60, id='reminder_job', replace_existing=True)

if __name__ == '__main__':
    app.run(debug=True)
