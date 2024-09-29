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
                window.location.href = '/schedules/schedules-page';
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
