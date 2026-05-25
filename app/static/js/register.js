document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = form.username.value.trim();
        const password = form.password.value;
        const gender = form.gender.value;

        if (!username || !password) {
            alert('用户名和密码为必填项。');
            return;
        }
        if (password.length < 6) {
            alert('密码长度至少为 6 位。');
            return;
        }

        const existingUserResult = await fetch(`/api/user/${encodeURIComponent(username)}`);
        if (existingUserResult.ok) {
            const existingUser = await existingUserResult.json();
            alert('该用户名已被使用。');
            return;
        }

        const createResult = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, gender }),
        });
        if (createResult.ok) {
            alert('注册成功，正在跳转...');
            window.location.href = '/login';
        } else {
            alert('注册失败。');
        }
    });
});
