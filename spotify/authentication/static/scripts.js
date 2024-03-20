document.addEventListener('DOMContentLoaded', () => {
    const spotifyApiButton = document.getElementById('spotifyApiButton');
    const sliders = document.querySelectorAll('input[type="range"]');

    spotifyApiButton.addEventListener('click', async () => {
        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const sliderValues = {};
            sliders.forEach(slider => {
                sliderValues[slider.id] = parseFloat(slider.value);
            });
            const payload = JSON.stringify({ sliders: sliderValues });

            const response = await fetch('/playlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: payload,
            });

            if (!response.ok) {
                throw new Error('Failed to fetch data from Spotify API');
            }
            const data = await response.json();
            console.log('Data from Spotify API:', data);
        } catch (error) {
            console.error('Error fetching data from Spotify API:', error);
            // Handle the error, show an error message, or retry the request
        }
    });
});
