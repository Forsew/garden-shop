const API_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    
    if (!form) {
        console.error('Форма регистрации не найдена');
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const errorDiv = document.getElementById('errorMessage');
        const successDiv = document.getElementById('successMessage');
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';

        // Собираем данные формы согласно схеме UserRegistration
        const formData = {
            username: document.getElementById('username').value.trim(),
            full_name: document.getElementById('fio').value.trim(),
            password: document.getElementById('password').value,
            birth_date: document.getElementById('birth_date').value,
            address: document.getElementById('address').value.trim(),
            gender: document.getElementById('gender').value === 'men' ? 'Мужской' : 'Женский',
            hobby: document.getElementById('interests').value.trim() || null,
            vk_profile: document.getElementById('vk_link').value.trim() || null,
            blood_group: document.getElementById('blood_group').value,
            rh_factor: document.getElementById('rh_factor').value.trim()
        };

        // Простая валидация на фронтенде
        if (!formData.username.startsWith('@')) {
            errorDiv.textContent = 'Username должен начинаться с @';
            errorDiv.style.display = 'block';
            return;
        }

        // Убираем @ из username перед отправкой
        formData.username = formData.username.substring(1);

        try {
            const response = await fetch(`${API_URL}/api/auth/reg`, {
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
                localStorage.setItem('user', JSON.stringify(data.user));

                successDiv.textContent = 'Регистрация успешна! Перенаправление...';
                successDiv.style.display = 'block';

                // Перенаправление через 2 секунды
                setTimeout(() => {
                    window.location.href = 'profile.html';
                }, 2000);
            } else {
                // Обработка ошибок валидации
                if (data.detail) {
                    if (Array.isArray(data.detail)) {
                        errorDiv.textContent = data.detail.map(err => err.msg).join(', ');
                    } else {
                        errorDiv.textContent = data.detail;
                    }
                } else {
                    errorDiv.textContent = 'Ошибка регистрации';
                }
                errorDiv.style.display = 'block';
            }
        } catch (error) {
            errorDiv.textContent = 'Ошибка соединения с сервером. Убедитесь, что backend запущен.';
            errorDiv.style.display = 'block';
            console.error('Error:', error);
        }
    });
});