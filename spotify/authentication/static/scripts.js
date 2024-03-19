let a = 0.5; // Initial value for a
let b = 0.5; // Initial value for b
let c = 0.5; // Initial value for c

const sliders = document.querySelectorAll('input[type="range"]');

sliders.forEach(slider => {
    slider.addEventListener('input', () => {
        // Update variables a, b, or c based on slider id
        if (slider.id === 'melancholic') {
            a = parseFloat(slider.value);
        } else if (slider.id === 'electronic') {
            b = parseFloat(slider.value);
        } else if (slider.id === 'energy') {
            c = parseFloat(slider.value);
        }

        // Print updated values of a, b, and c in the console
        console.log('Updated values:');
        console.log('a:', a);
        console.log('b:', b);
        console.log('c:', c);

        // Call updateColor function or perform other actions as needed
        updateColor();
    });
});

function updateColor() {
    // Update color grid or perform other actions based on variables a, b, c
    console.log('Updating color grid or performing other actions...');
}