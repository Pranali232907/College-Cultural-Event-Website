// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto close alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Star rating display
    const starRatings = document.querySelectorAll('.star-rating');
    starRatings.forEach(function(container) {
        const rating = parseInt(container.dataset.rating, 10);
        const stars = container.querySelectorAll('.fa-star');

        stars.forEach(function(star, index) {
            if (index < rating) {
                star.classList.remove('empty');
            } else {
                star.classList.add('empty');
            }
        });
    });

    // Image gallery lightbox (if used)
    const galleryImages = document.querySelectorAll('.gallery-item img');
    galleryImages.forEach(function(image) {
        image.addEventListener('click', function() {
            const src = this.getAttribute('src');
            const lightbox = document.createElement('div');
            lightbox.id = 'lightbox';
            lightbox.innerHTML = `
                <div class="lightbox-container">
                    <img src="${src}" alt="Enlarged image">
                    <span class="close-lightbox">&times;</span>
                </div>
            `;

            document.body.appendChild(lightbox);
            document.body.style.overflow = 'hidden';

            lightbox.addEventListener('click', function(e) {
                if (e.target.id === 'lightbox' || e.target.classList.contains('close-lightbox')) {
                    document.body.removeChild(lightbox);
                    document.body.style.overflow = '';
                }
            });
        });
    });

    // Form validation for contact form
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            const name = document.getElementById('id_name');
            const email = document.getElementById('id_email');
            const message = document.getElementById('id_message');
            let valid = true;

            if (!name.value.trim()) {
                valid = false;
                name.classList.add('is-invalid');
            } else {
                name.classList.remove('is-invalid');
            }

            if (!email.value.trim() || !isValidEmail(email.value)) {
                valid = false;
                email.classList.add('is-invalid');
            } else {
                email.classList.remove('is-invalid');
            }

            if (!message.value.trim()) {
                valid = false;
                message.classList.add('is-invalid');
            } else {
                message.classList.remove('is-invalid');
            }

            if (!valid) {
                event.preventDefault();
            }
        });
    }

    // Helper function to validate email format
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
});