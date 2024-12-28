// static/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // File upload handling
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const maxSize = 10 * 1024 * 1024; // 10MB
                if (file.size > maxSize) {
                    alert('File size exceeds 10MB limit');
                    e.target.value = '';
                    return;
                }

                const fileLabel = document.querySelector('.custom-file-label');
                if (fileLabel) {
                    fileLabel.textContent = file.name;
                }
            }
        });
    }

    // Alert auto-hide with fade effect
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease-out';
            alert.style.opacity = '0';
            setTimeout(() => {
                const parent = alert.parentElement;
                if (parent) {
                    parent.removeChild(alert);
                }
            }, 500);
        }, 5000);
    });

    // Table sorting functionality
    const tables = document.querySelectorAll('.table-sortable');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const column = header.dataset.sort;
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                const direction = header.classList.contains('sort-asc') ? -1 : 1;

                rows.sort((a, b) => {
                    const aValue = a.querySelector(`td[data-${column}]`)?.textContent || '';
                    const bValue = b.querySelector(`td[data-${column}]`)?.textContent || '';
                    return aValue.localeCompare(bValue) * direction;
                });

                headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
                header.classList.toggle('sort-asc', direction === 1);
                header.classList.toggle('sort-desc', direction === -1);

                const tbody = table.querySelector('tbody');
                if (tbody) {
                    tbody.innerHTML = '';
                    rows.forEach(row => tbody.appendChild(row));
                }
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();

                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
            form.classList.add('was-validated');
        });

        // Real-time validation feedback
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('input', function () {
                if (field.value.trim()) {
                    field.classList.remove('is-invalid');
                } else {
                    field.classList.add('is-invalid');
                }
            });
        });
    });
});