document.addEventListener('DOMContentLoaded', () => {
    async function fetchFriends() {
        const friendsContainer = document.getElementById('friendsContainer');
        try {
            const res = await fetch('/api/friends', { method: 'GET' });
            if (res.ok) {
                const friends = await res.json();
                console.log("friends list:", friends);
                friendsContainer.innerHTML = '';
                if (friends.length === 0) {
                    friendsContainer.innerHTML += '<p>当前没有好友。</p>';
                    return;
                }
                for (const friend of friends) {
                    friendsContainer.innerHTML += `
                        <div class="friend">
                            <a href="/user/${friend.user_id}" target="_blank">
                                <h3>${friend.username}</h3>
                            </a>
                            <p class="timestamp">成为好友时间: ${friend.created_at}</p>
                        </div>
                    `;
                }
            }
            else {
                console.error('Failed to load posts:', res.status);
                friendsContainer.innerHTML = '<p>好友加载失败。</p>';
            }
        } catch (error) {
            console.error('Error fetching friends:', error);
            friendsContainer.innerHTML = '<p>好友加载失败。</p>';
        }
    }

    fetchFriends();
});