document.addEventListener('DOMContentLoaded', function() {
    // Universal Form Validation
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

    // Universal Card Interactions
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', function(e) {
            if (this.querySelector('a')) {
                this.querySelector('a').click();
            }
        });
    });

    // Universal Search Handling
    const searchInputs = document.querySelectorAll('.global-search');
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce((e) => {
            e.target.form.submit();
        }, 500));
    });
});

function debounce(func, timeout = 300){
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}