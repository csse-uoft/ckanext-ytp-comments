window.addEventListener('load', () => {
    const forms = document.querySelectorAll('.needs-validation');

    for (const form of forms) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    }

});
