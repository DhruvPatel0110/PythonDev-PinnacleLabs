const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
let today = new Date();
let currentYear = today.getFullYear();
let currentMonth = today.getMonth();
let selectedDay = null;

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

// Initial render
renderCalendar(currentYear, currentMonth);
