document.addEventListener('DOMContentLoaded', function () {

    const removeBtn = document.querySelector('.btn-remove');
    const inputs = document.querySelectorAll('input[type="text"]');

    removeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        inputs.forEach(item => item.value = '');
    });
}
);