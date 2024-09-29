const reserveButtons = document.querySelectorAll('.reserve-btn');
if (reserveButtons) {
    reserveButtons.forEach(button => {
        button.addEventListener('click', async function () {
            if (confirm("Are you sure you want to reserve this seat?")) {
                const seatId = button.getAttribute('data-seat-id');
                const scheduleId = button.getAttribute('data-schedule-id');

                try {
                    const response = await fetch('/reservations/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            seat_id: seatId,
                            schedule_id: scheduleId
                        })
                    });

                    if (response.ok) {
                        location.reload()
                    } else {
                        const errorData = await response.json();
                        console.log(errorData);
                        alert('Error occurred, please see console for details.');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('An error occurred while reserving the seat.');
                }
            }
        });
    });
}

document.querySelectorAll('.deleteReservation').forEach(button => {
    button.addEventListener('click', async function (event) {
        event.stopPropagation();

        const reservationId = this.getAttribute('data-reservation-id');
        const confirmed = confirm("Are you sure you want to delete this reservation?");


        if (confirmed) {
            try {
                const response = await fetch(`/reservations/${reservationId}`, {
                    method: 'DELETE',
                });

                if (response.ok) {
                    window.location.reload();
                } else {
                    const errorData = await response.json();
                    console.log(errorData);
                    alert('Error occurred, please see console for details.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while deleting the reservation.');
            }
        }
    });
});