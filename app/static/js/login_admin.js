document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const admin_id = form.admin_id.value.trim();
        const password = form.password.value;

        if (!admin_id || !password) {
            alert('管理员id和密码为必填项。');
        }

        const loginResult = await fetch('/login/admin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ admin_id, password }),
        });
        if (loginResult.ok) {
            alert('登录成功，正在跳转...');
            window.location.href = '/';
        } else {
            alert('登录失败。');
        }
    });
});
