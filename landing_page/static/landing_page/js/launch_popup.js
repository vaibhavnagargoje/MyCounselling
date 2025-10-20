document.addEventListener('DOMContentLoaded', function() {
    // Launch Popup Logic
    const launchPopup = document.getElementById('launch-popup');
    const closePopupBtn = document.getElementById('close-popup-btn');
    const popupCard = launchPopup.querySelector('.popup-card');

    if (!sessionStorage.getItem('popupDismissed')) {
        setTimeout(() => {
            launchPopup.classList.remove('hidden');
            setTimeout(() => {
                launchPopup.classList.add('opacity-100');
                popupCard.classList.add('active');
            }, 50);
        }, 1000); // Show after 1 second
    }

    const dismissPopup = () => {
        launchPopup.classList.remove('opacity-100');
        popupCard.classList.remove('active');
        setTimeout(() => {
            launchPopup.classList.add('hidden');
        }, 300);
        sessionStorage.setItem('popupDismissed', 'true');
    };

    closePopupBtn.addEventListener('click', dismissPopup);
    launchPopup.addEventListener('click', (e) => {
        if (e.target === launchPopup) {
            dismissPopup();
        }
    });
});
