document.addEventListener('DOMContentLoaded', function () {
    const sliders = document.querySelectorAll('input[type="range"]');
    const values = document.querySelectorAll('span');

    sliders.forEach((slider, index) => {
        slider.addEventListener('input', function () {
            values[index].textContent = this.value;
        });
    });

    const saveBtn = document.getElementById('saveBtn');
    saveBtn.addEventListener('click', function () {
        const melancholicCheerfulValue = parseFloat(document.getElementById('melancholicCheerful').value);
        const electronicOrganicValue = parseFloat(document.getElementById('electronicOrganic').value);
        const lowHighEnergyValue = parseFloat(document.getElementById('lowHighEnergy').value);
        
        // You can use these variables to save the values to your backend or perform further actions
        console.log('Melancholic vs Cheerful:', melancholicCheerfulValue);
        console.log('Electronic vs Organic:', electronicOrganicValue);
        console.log('Low Energy vs High Energy:', lowHighEnergyValue);
    });
});
