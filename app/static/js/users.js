document.addEventListener('DOMContentLoaded', () => {
    async function fetchUsers() {
        const usersContainer = document.getElementById('usersContainer');
        try {
            const res = await fetch('/api/users', { method: 'GET' });
            if (res.ok) {
                const users = await res.json();
                console.log("users list:", users);
                usersContainer.innerHTML = '';
                if (users.length === 0) {
                    usersContainer.innerHTML += '<p>当前没有用户。</p>';
                    return;
                }
                for (const user of users) {
                    usersContainer.innerHTML += `
                        <div class="user">
                            <a href="/user/${user.user_id}" target="_blank">
                                <h3>${user.username}</h3>
                            </a>
                        </div>
                    `;
                }
            }
            else {
                console.error('Failed to load posts:', res.status);
                usersContainer.innerHTML = '<p>好友加载失败。</p>';
            }
        } catch (error) {
            console.error('Error fetching friends:', error);
            usersContainer.innerHTML = '<p>好友加载失败。</p>';
        }
    }

    fetchUsers();
});