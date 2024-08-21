document.addEventListener('DOMContentLoaded', function() {
    const registerBtn = document.getElementById('registerBtn');
    const loginBtn = document.getElementById('loginBtn');
    let registerForm = null;
    let loginForm = null;

    registerBtn.addEventListener('click', function() {
        if (loginForm) {
            loginForm.remove();
            loginForm = null;
        }

        if (registerForm && registerForm.style.display === 'block') {
            registerForm.remove();
            registerForm = null;
            return;
        }

        fetch('/register/')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                registerForm = doc.querySelector('#registerPopupForm');

                document.body.appendChild(registerForm);
                registerForm.style.display = 'block';

                const closeBtn = registerForm.querySelector('#closeBtn');
                closeBtn.addEventListener('click', function() {
                    registerForm.remove();
                    registerForm = null;
                });
            });
    });

    loginBtn.addEventListener('click', function() {
        if (registerForm) {
            registerForm.remove();
            registerForm = null;
        }

        if (loginForm && loginForm.style.display === 'block') {
            loginForm.remove();
            loginForm = null;
            return;
        }

        fetch('/login/')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                loginForm = doc.querySelector('#popupForm');

                document.body.appendChild(loginForm);
                loginForm.style.display = 'block';

                const closeBtn = loginForm.querySelector('#closeBtn');
                closeBtn.addEventListener('click', function() {
                    loginForm.remove();
                    loginForm = null;
                });
            });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const errorMessage = document.querySelector('.error-message');
    const registerPopupForm = document.getElementById('registerPopupForm');
    
    if (errorMessage) {
        registerPopupForm.style.display = 'block';
    }
});