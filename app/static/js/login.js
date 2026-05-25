document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = form.username.value.trim();
        const password = form.password.value;

        if (!username || !password) {
            alert('用户名和密码为必填项。');
        }

        const loginResult = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        if (loginResult.ok) {
            alert('登录成功，正在跳转...');
            window.location.href = '/';
        } else {
            alert('登录失败。');
        }
    });
});
