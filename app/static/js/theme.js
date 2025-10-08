document.addEventListener('DOMContentLoaded', () => {
    const themeSwitcher = document.getElementById('theme-switcher');
    const body = document.body;

    const savedTheme = localStorage.getItem('theme');

    if (savedTheme) {
        body.classList.add(savedTheme);
    }

    themeSwitcher.addEventListener('click', () => {
        if (body.classList.contains('dark-theme')) {
            body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light-theme');
        } else {
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark-theme');
        }
    });
});
