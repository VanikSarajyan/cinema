const createScheduleForm = document.getElementById('scheduleCreateForm');
if (createScheduleForm) {
    createScheduleForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        const data = Object.fromEntries(formData.entries());

        const payload = {
            movie_id: parseInt(data.movie_id),
            room_id: parseInt(data.room_id),
            start_time: data.start_time,
            end_time: data.end_time
        };

        console.log(payload);

        try {
            const response = await fetch('/schedules/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.history.go(-1)
            } else {
                const errorData = await response.json();
                console.log(errorData);
                alert('Error occurred, please see console for details.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}


document.querySelectorAll('.deleteSchedule').forEach(button => {
    button.addEventListener('click', async function (event) {
        event.stopPropagation();

        const scheduleId = this.getAttribute('data-schedule-id');
        const confirmed = confirm("Are you sure you want to delete this schedule?");


        if (confirmed) {
            try {
                const response = await fetch(`/schedules/${scheduleId}`, {
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
                alert('An error occurred while deleting the schedule.');
            }
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const movieSelect = document.getElementById('movie_id');
    const startTimeInput = document.getElementById('start_time');
    const endTimeInput = document.getElementById('end_time');

    function addMinutesAndRound(startTime, minutesToAdd) {
        const start = new Date(startTime);

        if (!start || isNaN(start.getTime())) {
            console.error("Invalid start time.");
            return;
        }

        start.setMinutes(start.getMinutes() + minutesToAdd);

        let minutes = start.getMinutes();

        let roundedMinutes = Math.ceil(minutes / 10) * 10;
        if (roundedMinutes === 60) {
            start.setHours(start.getHours() + 1);
            roundedMinutes = 0;
        }

        start.setMinutes(roundedMinutes);

        const year = start.getFullYear();
        const month = String(start.getMonth() + 1).padStart(2, '0');
        const day = String(start.getDate()).padStart(2, '0');
        const hours = String(start.getHours()).padStart(2, '0');
        const minutesFormatted = String(start.getMinutes()).padStart(2, '0');

        const formattedEndTime = `${year}-${month}-${day}T${hours}:${minutesFormatted}`;

        endTimeInput.value = formattedEndTime;

    }

    movieSelect.addEventListener('change', function () {
        const selectedMovie = movieSelect.options[movieSelect.selectedIndex];
        const movieDuration = parseInt(selectedMovie.getAttribute('data-duration'), 10);

        if (startTimeInput.value && !isNaN(movieDuration)) {
            addMinutesAndRound(startTimeInput.value, movieDuration);
        }
    });

    startTimeInput.addEventListener('change', function () {
        const selectedMovie = movieSelect.options[movieSelect.selectedIndex];
        const movieDuration = parseInt(selectedMovie.getAttribute('data-duration'), 10);

        if (movieDuration && !isNaN(movieDuration)) {
            addMinutesAndRound(startTimeInput.value, movieDuration);
        }
    });
});
