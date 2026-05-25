document.addEventListener('DOMContentLoaded', () => {
    const postsContainer = document.getElementById('postsContainer');
    const target_id = postsContainer.dataset.targetId;
    async function fetchPosts() {
        try {
            const res = await fetch(`/api/posts/${target_id}`, { method: 'GET' });
            if (res.ok) {
                const res_json = await res.json();
                const posts = res_json.posts_list;
                const username = res_json.username;
                const visibility = { "public": "公开", "friends": "仅好友可见", "private": "仅自己可见" };
                console.log('Posts data:', res_json);
                postsContainer.innerHTML = `<h1>${username} 的朋友圈</h1>`;
                if (posts.length === 0) {
                    postsContainer.innerHTML += '<p>当前没有朋友圈。</p>';
                } else {
                    for (const post of posts) {
                        postsContainer.innerHTML += `
                            <div class="post" data-post-id="${post.post_id}">
                                <a href="/user/${target_id}" target="_blank">
                                    <h4>${username}</h4>
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

    const form = document.getElementById('postForm');
    const wordLimit = 200;
    const content = form.content;
    const wordCountDisplay = form.getElementsByClassName('word_limit')[0];

    form.addEventListener('input', () => {
        const currentLength = content.value.length;
        wordCountDisplay.textContent = `${currentLength}/${wordLimit}`;
        if (currentLength > wordLimit) {
            wordCountDisplay.style.color = 'red';
        } else {
            wordCountDisplay.style.color = '#6b778c';
        }
    })

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const text = content.value.trim();
        const visibility = form.visibility.value;
        if (!text) {
            alert('内容不能为空');
            return;
        }
        if (text.length > wordLimit) {
            alert(`内容不能超过 ${wordLimit} 字`);
            return;
        }
        try {
            const res = await fetch(`/api/posts/${target_id}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: text, visibility: visibility }),
            });
            if (res.ok) {
                const newPost = await res.json();
                content.value = '';
                wordCountDisplay.textContent = `0/${wordLimit}`;
                wordCountDisplay.style.color = '#6b778c';
                alert('朋友圈发布成功');
                fetchPosts();
            } else {
                alert('朋友圈发布失败');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('发布朋友圈时发生错误');
        }
    });
});