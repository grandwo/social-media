document.addEventListener('DOMContentLoaded', () => {
    const commentsContainer = document.getElementById('commentsContainer');
    const comment_id = commentsContainer.dataset.commentId
    const user_id = commentsContainer.dataset.userId
    const role = commentsContainer.dataset.role

    async function fetchComment() {
        try {
            const res = await fetch(`/api/comment/${comment_id}`, { method: 'GET' });
            if (res.ok) {
                const comment = await res.json();
                console.log("comment:", comment);
                if (!comment) {
                    commentsContainer.innerHTML = '<p>无法查看该条评论</p>';
                } else {
                    commentsContainer.innerHTML = `
                        <div class="comment">
                            <a href="/user/${comment.user_id}" target="_blank">
                                <h4>${comment.username}</h4>
                            </a>
                            <p>${comment.content}</p>
                            <span class="timestamp">评论于 ${new Date(comment.created_at).toLocaleString()}</span>
                        </div>
                    `;
                    if (role === "admin") {
                        commentsContainer.innerHTML += `
                            <p style="gap:15px">
                                <button id="delete">删除</button>
                            </p>
                        `;
                    }
                    else if (comment.user_id == user_id) {
                        commentsContainer.innerHTML += `
                            <p style="gap:15px">
                                <button id="delete">删除</button>
                            </p>
                        `;
                    }
                }
            }
            else {
                console.error("Error:", res.error);
                commentsContainer.innerHTML += '<p>评论加载失败。</p>';
            }
        }
        catch (error) {
            console.error("Error:", error);
            commentsContainer.innerHTML += '<p>评论加载失败。</p>';
        }
    }


    commentsContainer.addEventListener('click', async (event) => {
        if (event.target.id === "delete") {
            try {
                const res = await fetch(`/api/comment/${comment_id}`, { method: 'DELETE' });
                if (res.ok) {
                    alert("删除成功")
                    fetchComment();
                } else {
                    alert('删除失败');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('删除时发生错误');
            }
        }
    });

    fetchComment()
});