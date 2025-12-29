// Batch Dropdown Functionality
document.addEventListener('DOMContentLoaded', function() {
    const batchDropdown = document.getElementById('batchDropdown');
    const batchMenu = document.getElementById('batchMenu');
    const dropdownIcon = document.getElementById('dropdownIcon');
    const selectedBatch = document.getElementById('selectedBatch');
    const batchOptions = document.querySelectorAll('.batch-option');

    if (batchDropdown) {
        batchDropdown.addEventListener('click', () => {
            batchMenu.classList.toggle('active');
            dropdownIcon.classList.toggle('rotate-180');
        });
    }

    if (batchOptions) {
        batchOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.preventDefault();
                const batchName = option.getAttribute('data-batch');
                selectedBatch.textContent = batchName;
                batchMenu.classList.remove('active');
                dropdownIcon.classList.remove('rotate-180');
            });
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (batchDropdown && !batchDropdown.contains(e.target)) {
            if (batchMenu) batchMenu.classList.remove('active');
            if (dropdownIcon) dropdownIcon.classList.remove('rotate-180');
        }
    });

    // Mobile Sidebar Functionality
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');

    function toggleSidebar() {
        if (!sidebar || !sidebarOverlay) return;
        
        const isClosed = sidebar.classList.contains('-translate-x-full');
        
        if (isClosed) {
            // Open sidebar
            sidebar.classList.remove('-translate-x-full');
            sidebarOverlay.classList.remove('hidden');
            // Small delay to allow display:block to apply before opacity transition
            setTimeout(() => {
                sidebarOverlay.classList.remove('opacity-0');
            }, 10);
        } else {
            // Close sidebar
            sidebar.classList.add('-translate-x-full');
            sidebarOverlay.classList.add('opacity-0');
            setTimeout(() => {
                sidebarOverlay.classList.add('hidden');
            }, 300);
        }
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }
});
