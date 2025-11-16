const API_URL = 'http://localhost:8000';

document.getElementById('registrationForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const errorDiv = document.getElementById('errorMessage');
    const successDiv = document.getElementById('successMessage');
    errorDiv.style.display = 'none';
    successDiv.style.display = 'none';

    const formData = {
        phone: document.getElementById('phone').value,
        fio: document.getElementById('fio').value,
        birth_date: document.getElementById('birth_date').value,
        address: document.getElementById('address').value,
        gender: document.getElementById('gender').value,
        interests: document.getElementById('interests').value,
        vk_link: document.getElementById('vk_link').value,
        blood_group: document.getElementById('blood_group').value,
        rh_factor: document.getElementById('rh_factor').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch(`${API_URL}/api/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            // Сохраняем токен
            localStorage.setItem('access_token', data.access_token);

            successDiv.textContent = 'Регистрация успешна! Перенаправление...';
            successDiv.style.display = 'block';

            // Перенаправление через 2 секунды
            setTimeout(() => {
                window.location.href = 'profile.html';
            }, 2000);
        } else {
            errorDiv.textContent = data.detail || 'Ошибка регистрации';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'Ошибка соединения с сервером';
        errorDiv.style.display = 'block';
        console.error('Error:', error);
    }
});
