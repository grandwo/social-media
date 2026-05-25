document.addEventListener('DOMContentLoaded', () => {
    const postsContainer = document.getElementById('postsContainer');
    async function fetchPosts() {
        try {
            const res = await fetch(`/api/posts`, { method: 'GET' });
            if (res.ok) {
                const posts = await res.json();
                const visibility = { "public": "公开", "friends": "仅好友可见", "private": "仅自己可见" };
                console.log('Posts data:', posts);
                postsContainer.innerHTML = ``;
                if (posts.length === 0) {
                    postsContainer.innerHTML += '<p>当前没有朋友圈。</p>';
                } else {
                    for (const post of posts) {
                        postsContainer.innerHTML += `
                            <div class="post" data-post-id="${post.post_id}">
                                <a href="/user/${post.user_id}" target="_blank">
                                    <h4>${post.username}</h4>
                                </a>
                                <a href="/post/${post.post_id}" target="_blank">
                                    <p>${post.content}</p>
                                </a>
                                <span class="timestamp">最后修改于 ${new Date(post.updated_at).toLocaleString()}</span>
                                <span class="visibility-stamp">${visibility[post.visibility]}</span>
                            </div>
                        `;
                    }
                }
            } else {
                console.error('Failed to load posts:', res.status);
                postsContainer.innerHTML = '<p>朋友圈加载失败。</p>';
            }
        } catch (error) {
            console.error('Error:', error);
            postsContainer.innerHTML = '<p>朋友圈加载失败。</p>';
        };
    }

    fetchPosts();
});