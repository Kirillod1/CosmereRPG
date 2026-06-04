document.addEventListener('DOMContentLoaded', () => {
    // Funkcja zarządzająca wyglądem paska nawigacji
    function updateNavbar() {
        const authButtons = document.getElementById('authButtons');
        const userMenu = document.getElementById('userMenu');
        const userDropdown = document.getElementById('userDropdown');
        
        // Sprawdzamy, czy w pamięci przeglądarki jest zapisana nazwa użytkownika
        const username = localStorage.getItem('username');

        if (username) {
            // Użytkownik Zalogowany: Ukryj przyciski, pokaż menu
            authButtons.classList.add('d-none');
            userMenu.classList.remove('d-none');
            userDropdown.textContent = 'Witaj, ' + username;
        } else {
            // Brak użytkownika (Gość): Pokaż przyciski, ukryj menu
            authButtons.classList.remove('d-none');
            userMenu.classList.add('d-none');
        }
    }

    // Uruchomienie funkcji przy każdym załadowaniu strony
    updateNavbar();

    // Obsługa wylogowania
    const btnLogout = document.getElementById('btnLogout');
    if (btnLogout) {
        btnLogout.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('username'); // Kasujemy dane z pamięci
            updateNavbar(); // Odświeżamy widok
        });
    }
    
    const form = document.getElementById('registerForm');
    const messageEl = document.getElementById('regMessage');
    
    // Inicjalizacja modala Bootstrapa z poziomu JS (żeby móc go zamknąć skryptem po sukcesie)
    const registerModalElement = document.getElementById('registerModal');
    const registerModal = new bootstrap.Modal(registerModalElement);

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); 

        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;

        try {
            const response = await fetch('/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                messageEl.className = "text-center mt-3 mb-0 small text-success"; 
                messageEl.textContent = data.message;
                form.reset(); 
                
                // Zamykamy okienko po 2 sekundach
                setTimeout(() => {
                    registerModal.hide();
                    messageEl.textContent = '';
                }, 2000);
            } else {
                messageEl.className = "text-center mt-3 mb-0 small text-danger";
                messageEl.textContent = data.detail || 'Wystąpił błąd przy rejestracji.';
            }
        } catch (error) {
            messageEl.className = "text-center mt-3 mb-0 small text-danger";
            messageEl.textContent = 'Błąd połączenia z serwerem.';
        }
    });
    // --- OBSŁUGA LOGOWANIA ---
    const loginForm = document.getElementById('loginForm');
    const logMessageEl = document.getElementById('logMessage');
    const loginModalElement = document.getElementById('loginModal');
    const loginModal = new bootstrap.Modal(loginModalElement);

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault(); 

        const login = document.getElementById('logLogin').value;
        const password = document.getElementById('logPassword').value;

        try {
            const response = await fetch('/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ login, password })
            });

            const data = await response.json();

            if (response.ok) {
                logMessageEl.className = "text-center mt-3 mb-0 small text-success"; 
                logMessageEl.textContent = data.message;
                loginForm.reset(); 
                
                // Zapisujemy nazwę gracza w pamięci przeglądarki
                localStorage.setItem('username', data.username);
                // Odświeżamy Navbar natychmiast po zalogowaniu
                updateNavbar();

                setTimeout(() => {
                    loginModal.hide();
                    logMessageEl.textContent = '';
                }, 1500);
            } else {
                logMessageEl.className = "text-center mt-3 mb-0 small text-danger";
                logMessageEl.textContent = data.detail || 'Błąd logowania.';
            }
        } catch (error) {
            logMessageEl.className = "text-center mt-3 mb-0 small text-danger";
            logMessageEl.textContent = 'Błąd połączenia z serwerem.';
        }
    });
});