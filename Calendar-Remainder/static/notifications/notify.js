// Browser Notification System for Calendar Reminder App

// Request notification permission on page load
function requestNotificationPermission() {
    if ('Notification' in window) {
        if (Notification.permission === 'default') {
            Notification.requestPermission().then(function(permission) {
                console.log('Notification permission:', permission);
            });
        }
    }
}

// Show a browser/system notification
function showReminderNotification(title, body) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, { body: body, icon: '/static/notifications/reminder.png' });
    }
}

// Example: Call this when a reminder is due
// showReminderNotification('Reminder', 'Attend Meeting at 18:00');

// Request permission on load
window.addEventListener('DOMContentLoaded', requestNotificationPermission);
