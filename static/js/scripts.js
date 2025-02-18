document.addEventListener('DOMContentLoaded', function () {
    // Auto-submit search forms after typing stops
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        let timeoutId;
        input.addEventListener('input', function () {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                if (input.value.trim() !== '') {
                    input.form.submit();
                }
            }, 500);
        });
    });

    // Add hover effects to cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});