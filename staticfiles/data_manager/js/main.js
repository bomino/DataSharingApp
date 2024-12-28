// static/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    // File upload preview
    const fileInput = document.querySelector('input[type="file"]');

    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const fileName = e.target.files[0]?.name;
            const fileSize = e.target.files[0]?.size;
            const maxSize = 10 * 1024 * 1024; // 10MB

            if (fileSize > maxSize) {
                alert('File size exceeds 10MB limit');
                e.target.value = '';
                return;
            }

            const fileLabel = document.querySelector('.custom-file-label');

            if (fileLabel) {
                fileLabel.textContent = fileName || 'Choose file';
            }
        });
    }

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }

            , 5000);
    });

    // Table sorting
    const tables = document.querySelectorAll('.table-sortable');

    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');

        headers.forEach(header => {
            header.addEventListener('click', () => {
                const column = header.dataset.sort;
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                const direction = header.classList.contains('sort-asc') ? -1 : 1;

                rows.sort((a, b) => {
                    const aValue = a.querySelector(`td[data-$ {
                                                column
                                            }

                                            ]`).textContent;

                    const bValue = b.querySelector(`td[data-$ {
                                                column
                                            }

                                            ]`).textContent;
                    return aValue.localeCompare(bValue) * direction;
                });

                headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
                header.classList.toggle('sort-asc', direction === 1);
                header.classList.toggle('sort-desc', direction === -1);

                const tbody = table.querySelector('tbody');
                tbody.innerHTML = '';
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                }

                else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.is-invalid');

                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
        });
    });
});

// Form validation
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });
});