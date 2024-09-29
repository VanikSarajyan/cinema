const createMovieForm = document.getElementById('movieCreateForm');
if (createMovieForm) {
    createMovieForm.addEventListener('submit', async function (event) {
        console.log(event)
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        const data = Object.fromEntries(formData.entries());

        const payload = {
            name: data.name,
            poster: data.poster,
            description: data.description,
            active: data.active
        };

        console.log(payload)

        try {
            const response = await fetch('/movies/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = '/movies/movies-page';
            } else {
                const errorData = await response.json();
                console.log(errorData)
                alert(`Error occured, please see console for detals.`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

const editMovieForm = document.getElementById('movieEditForm');
if (editMovieForm) {
    editMovieForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const movieId = form.dataset.movieId;

        const data = Object.fromEntries(formData.entries());

        const payload = {
            name: data.name,
            poster: data.poster,
            description: data.description,
            active: data.active
        };

        try {
            const response = await fetch(`/movies/${movieId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {

                window.location.href = '/movies/movies-page';
            } else {
                const errorData = await response.json();
                console.log(errorData)
                alert(`Error occured, please see console for detals.`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

const deleteMovieButtons = document.getElementsByClassName('deleteMovie');
for (let i = 0; i < deleteMovieButtons.length; i++) {
    const button = deleteMovieButtons[i];
    button.addEventListener('click', async function () {
        const movieId = button.dataset.movieId;
        console.log(movieId);
        if (confirm('Are you sure you want to delete this movie?')) {
            try {
                const response = await fetch(`/movies/${movieId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    window.location.reload();
                } else {
                    const errorData = await response.json();
                    console.log(errorData)
                    alert(`Error occured, please see console for detals.`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        }
    });
}

document.querySelectorAll('.movieRow').forEach(row => {
    row.addEventListener('click', function () {
        const movieId = this.getAttribute('data-movie-id');
        const scheduleRow = document.getElementById(`schedule-${movieId}`);

        if (scheduleRow.style.display === "none") {
            scheduleRow.style.display = "table-row";
        } else {
            scheduleRow.style.display = "none";
        }
    });
});