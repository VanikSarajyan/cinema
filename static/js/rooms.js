document.querySelectorAll('.roomRow').forEach(row => {
    row.addEventListener('click', function () {
        const roomId = this.getAttribute('data-room-id');
        const scheduleRow = document.getElementById(`schedule-${roomId}`);

        // Toggle visibility of the schedule row
        if (scheduleRow.style.display === "none") {
            scheduleRow.style.display = "table-row";
        } else {
            scheduleRow.style.display = "none";
        }
    });
});