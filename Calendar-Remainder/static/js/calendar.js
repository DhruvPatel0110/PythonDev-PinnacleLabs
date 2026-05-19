const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
let today = new Date();
let currentYear = today.getFullYear();
let currentMonth = today.getMonth();
let selectedDay = null;

function updateYearMonthDisplay() {
    document.getElementById('currentYear').textContent = currentYear;
    document.getElementById('currentMonth').textContent = `${monthNames[currentMonth]} ${currentYear}`;
}

function renderCalendar(year, month) {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    let html = '<table class="table table-bordered"><thead><tr>';
    ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].forEach(d => html += `<th>${d}</th>`);
    html += '</tr></thead><tbody><tr>';
    for (let i = 0; i < firstDay.getDay(); i++) html += '<td></td>';
    for (let d = 1; d <= lastDay.getDate(); d++) {
        const date = new Date(year, month, d);
        let classes = [];
        if (date.toDateString() === today.toDateString()) classes.push('today');
        html += `<td class="${classes.join(' ')}" data-date="${date.toISOString()}">${d}</td>`;
        if ((date.getDay() + 1) % 7 === 0) html += '</tr><tr>';
    }
    html += '</tr></tbody></table>';
    document.getElementById('calendar').innerHTML = html;
    updateYearMonthDisplay();
    document.querySelectorAll('#calendar td[data-date]').forEach(td => {
        td.onclick = function() {
            selectedDay = new Date(this.dataset.date);
            showDayView(selectedDay);
        };
    });
}

function showDayView(date) {
    document.getElementById('selectedDate').textContent = `${date.getDate()} ${monthNames[date.getMonth()]} ${date.getFullYear()}`;
    document.getElementById('dayView').classList.remove('d-none');
}
function editReminder(id) {
    // Fetch reminder details and populate the edit form
    fetch(`/get_reminder/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const reminder = data.reminder;
                document.getElementById('dateTitle').value = reminder.title;
                document.getElementById('dateDate').value = reminder.reminder_date;
                document.getElementById('dateTime').value = reminder.reminder_time || '';
                document.getElementById('dateEmail').value = reminder.email;
                window.currentEditingReminderId = reminder.id;
                const editModal = new bootstrap.Modal(
                    document.getElementById('dateReminderModal')
                );
                editModal.show();
            } else {
                alert('Error fetching reminder details: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error fetching reminder details: ' + error.message);
        });
}

document.getElementById('prevYear').onclick = () => { currentYear--; renderCalendar(currentYear, currentMonth); };
document.getElementById('nextYear').onclick = () => { currentYear++; renderCalendar(currentYear, currentMonth); };
document.getElementById('prevMonth').onclick = () => {
    currentMonth--;
    if (currentMonth < 0) { currentMonth = 11; currentYear--; }
    renderCalendar(currentYear, currentMonth);
};
document.getElementById('nextMonth').onclick = () => {
    currentMonth++;
    if (currentMonth > 11) { currentMonth = 0; currentYear++; }
    renderCalendar(currentYear, currentMonth);
};

// Show modal on Remind Me button click
const remindMeBtn = document.getElementById('remindMeBtn');
if (remindMeBtn) {
    remindMeBtn.onclick = () => {
        const modal = new bootstrap.Modal(document.getElementById('reminderModal'));
        // Pre-fill date in Date Reminder form if a day is selected
        if (selectedDay) {
            const dateInput = document.getElementById('dateDate');
            if (dateInput) {
                dateInput.value = selectedDay.toISOString().slice(0, 10);
            }
        }
        modal.show();
    };
}

// Reminder History functionality
const reminderHistoryBtn = document.getElementById('reminderHistoryBtn');
if (reminderHistoryBtn) {
    reminderHistoryBtn.onclick = () => {
        const modal = new bootstrap.Modal(document.getElementById('historyModal'));
        loadReminderHistory();
        modal.show();
    };
}

// Load reminder history from backend
function loadReminderHistory() {
    fetch('/reminder_history')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('historyTableBody');
            tableBody.innerHTML = '';
            
            if (data.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No reminders yet</td></tr>';
                return;
            }
            
            data.forEach(reminder => {
                const row = `<tr>
                    <td>${reminder.title}</td>
                    <td><span class="badge bg-primary">${reminder.reminder_type}</span></td>
                    <td>${reminder.reminder_date}</td>
                    <td>${reminder.reminder_time || 'N/A'}</td>
                    <td>${reminder.email}</td>
                    <td><span class="badge ${reminder.notification_status === 'sent' ? 'bg-success' : 'bg-warning'}">${reminder.notification_status}</span></td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        })
        .catch(error => {
            console.error('Error loading reminder history:', error);
            document.getElementById('historyTableBody').innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error loading data</td></tr>';
        });
}

// Handle Date Reminder Form Submission
const dateReminderForm = document.getElementById('dateReminderForm');
if (dateReminderForm) {
    dateReminderForm.onsubmit = async (e) => {
        e.preventDefault();
        const data = {
            title: document.getElementById('dateTitle').value,
            reminder_type: 'date',
            reminder_date: document.getElementById('dateDate').value,
            reminder_time: document.getElementById('dateTime').value || null,
            email: document.getElementById('dateEmail').value
        };
        try {

    if (window.currentEditingReminderId) {

        const response = await fetch(
            `/edit_reminder/${window.currentEditingReminderId}`,
            {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }
        );

        const result = await response.json();

        if (result.success) {
            alert('Reminder Modified Successfully!');
            window.currentEditingReminderId = null;
            dateReminderForm.reset();

            bootstrap.Modal.getInstance(
                document.getElementById('reminderModal')
            ).hide();

            location.reload();

        } else {
            alert('Error: ' + result.error);
        }

        return;
    }

    // EXISTING ADD REMINDER CODE BELOW
    const response = await fetch('/add_reminder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (result.success) {
        alert('Reminder set successfully!');
        dateReminderForm.reset();

        bootstrap.Modal.getInstance(
            document.getElementById('reminderModal')
        ).hide();

    } else {
        alert('Error: ' + result.error);
    }

} catch (error) {
    alert('Error setting reminder: ' + error.message);
}
        try {
            const response = await fetch('/add_reminder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (result.success) {
                alert('Reminder set successfully!');
                dateReminderForm.reset();
                bootstrap.Modal.getInstance(document.getElementById('reminderModal')).hide();
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            alert('Error setting reminder: ' + error.message);
        }
    };
}

// Handle Time Reminder Form Submission
const timeReminderForm = document.getElementById('timeReminderForm');
if (timeReminderForm) {
    timeReminderForm.onsubmit = async (e) => {
        e.preventDefault();
        const data = {
            title: document.getElementById('timeTitle').value,
            reminder_type: 'time',
            reminder_date: new Date().toISOString().split('T')[0], // Today's date
            reminder_time: document.getElementById('timeTime').value,
            email: document.getElementById('timeEmail').value
        };
        
        try {
            const response = await fetch('/add_reminder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (result.success) {
                alert('Time reminder set successfully!');
                timeReminderForm.reset();
                bootstrap.Modal.getInstance(document.getElementById('reminderModal')).hide();
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            alert('Error setting reminder: ' + error.message);
        }
    };
}

// Initial render
renderCalendar(currentYear, currentMonth);
