class SliderValues {
    constructor() {
        this.sliders = document.querySelectorAll('input[type="range"]');
        this.sliderValues = {};

        this.sliders.forEach(slider => {
            this.sliderValues[slider.id] = parseFloat(slider.value);
            slider.addEventListener('input', this.updateSliderValue.bind(this, slider.id));
        });
    }

    updateSliderValue(sliderId) {
        const slider = document.getElementById(sliderId);
        this.sliderValues[sliderId] = parseFloat(slider.value);
        console.log(`Updated value of ${sliderId}: ${this.sliderValues[sliderId]}`);
        // You can perform additional actions here, such as updating UI elements or sending data to a server
    }

    getAllSliderValues() {
        return this.sliderValues;
    }
}

// Initialize the SliderValues class when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const sliderValues = new SliderValues();
    
    // Example of getting all slider values
    const allSliderValues = sliderValues.getAllSliderValues();
    console.log('All slider values:', allSliderValues);
});

document.addEventListener('DOMContentLoaded', () => {
    const spotifyApiButton = document.getElementById('spotifyApiButton');

    spotifyApiButton.addEventListener('click', async () => {
        try {
            // Make a fetch request to your backend endpoint that handles the Spotify API call
            const response = await fetch('/your-backend-endpoint-for-spotify-api');
            
            if (!response.ok) {
                throw new Error('Failed to fetch data from Spotify API');
            }

            // Parse the JSON response
            const data = await response.json();

            // Display or process the data received from the Spotify API
            console.log('Data from Spotify API:', data);
            // You can update the UI or perform additional actions with the data here

        } catch (error) {
            console.error('Error fetching data from Spotify API:', error);
            // Handle the error, show an error message, or retry the request
        }
    });
});
