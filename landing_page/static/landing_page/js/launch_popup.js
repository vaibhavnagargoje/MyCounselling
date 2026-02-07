document.addEventListener('DOMContentLoaded', function() {
    // Launch Popup Logic
    const launchPopup = document.getElementById('launch-popup');
    const closePopupBtn = document.getElementById('close-popup-btn');
    const popupCard = launchPopup.querySelector('.popup-card');

    // Countdown to March 1, 2026
    const launchDate = new Date('2026-03-01T00:00:00').getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = launchDate - now;

        if (distance < 0) {
            // Launch date has passed
            const countdownElement = document.getElementById('countdown');
            if (countdownElement) {
                countdownElement.innerHTML = '<span class="text-2xl font-bold text-green-400">🎉 We\'re Live Now!</span>';
            }
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        const countdownElement = document.getElementById('countdown');
        if (countdownElement) {
            countdownElement.innerHTML = `
                <div class="flex gap-4 justify-center">
                    <div class="text-center">
                        <div class="text-3xl font-bold text-white">${days}</div>
                        <div class="text-xs text-gray-300">Days</div>
                    </div>
                    <div class="text-3xl font-bold text-white">:</div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-white">${hours.toString().padStart(2, '0')}</div>
                        <div class="text-xs text-gray-300">Hours</div>
                    </div>
                    <div class="text-3xl font-bold text-white">:</div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-white">${minutes.toString().padStart(2, '0')}</div>
                        <div class="text-xs text-gray-300">Minutes</div>
                    </div>
                    <div class="text-3xl font-bold text-white">:</div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-white">${seconds.toString().padStart(2, '0')}</div>
                        <div class="text-xs text-gray-300">Seconds</div>
                    </div>
                </div>
            `;
        }
    }

    // Update countdown every second
    updateCountdown();
    setInterval(updateCountdown, 1000);

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
