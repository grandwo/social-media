document.addEventListener('DOMContentLoaded', () => {
    const postsContainer = document.getElementById('postsContainer');
    const post_id = postsContainer.dataset.postId
    const user_id = postsContainer.dataset.userId
    const role = postsContainer.dataset.role
    let canreview = false
    async function fetchPost() {
        try {
            const res = await fetch(`/api/post/${post_id}`, { method: 'GET' });
            if (res.ok) {
                const post = await res.json();
                console.log("post:", post);
                const visibility = { "public": "公开", "friends": "仅好友可见", "private": "仅自己可见" };
                if (!post) {
                    canreview = false
                    postsContainer.innerHTML = '<p>无法查看该条朋友圈</p>';
                } else {
                    canreview = true
                    postsContainer.innerHTML = `
                        <div class="post">
                            <a href="/user/${post.user_id}" target="_blank">
                                <h4>${post.username}</h4>
                            </a>
                            <p>${post.content}</p>
                            <span class="timestamp">最后修改于 ${new Date(post.updated_at).toLocaleString()}</span>
                            <span class="visibility-stamp">${visibility[post.visibility]}</span>
                        </div>
                    `;
                    if (role === "admin") {
                        postsContainer.innerHTML += `
                            <p style="gap:15px">
                                <button id="delete">删除</button>
                            </p>
                        `;
                    }
                    else if (post.user_id == user_id) {
                        postsContainer.innerHTML += `
                            <p style="gap:15px">
                                <button id="revised">修改</button>
                                <button id="delete">删除</button>
                            </p>
                        `;
                    }
                }
            }
            else {
                console.error("Error:", error);
                postsContainer.innerHTML = '<p>朋友圈加载失败。</p>';
            }
        }
        catch (error) {
            console.error("Error:", error);
            postsContainer.innerHTML = '<p>朋友圈加载失败。</p>';
        }
    }

    const commentsContainer = document.getElementById('commentsContainer');
    async function fetchComments() {
        commentsContainer.innerHTML = '';
        if (canreview) {
            if (role === "user") {
                commentsContainer.innerHTML += `
                    <form id="commentForm">
                        <textarea id="commentContent" name="content" rows="4" cols="10" placeholder="发布评论"></textarea>
                        <div class="word_limit">
                            0/200
                        </div>
                        <div class="actions" style="margin-top: 8px;">
                            <button id="commentButton" class="button">发布</button>
                        </div>
                    </form>
                `;
            }
            commentsContainer.innerHTML += '<h2>评论</h2>';
            try {
                const res = await fetch(`/api/comments/${post_id}`, { method: 'GET' });
                if (res.ok) {
                    const comments = await res.json();
                    console.log("comments:", comments);
                    if (comments.length === 0) {
                        commentsContainer.innerHTML += '<p>无评论</p>';
                    } else {
                        for (const comment of comments) {
                            commentsContainer.innerHTML += `
                                <div class="comment">
                                    <a href="/user/${comment.user_id}" target="_blank">
                                        <h4>${comment.username}</h4>
                                    </a>
                                    <a href="/comment/${comment.comment_id}" target="_blank">
                                        <p>${comment.content}</p>
                                    </a>
                                    <span class="timestamp">评论于 ${new Date(comment.created_at).toLocaleString()}</span>
                                </div>
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
    }


    async function myFetch() {
        await fetchPost();
        await fetchComments();
    }

    const wordLimit = 200;

    postsContainer.addEventListener('click', async (event) => {
        if (event.target.id === "revised") {
            postsContainer.innerHTML = `
                <form id="revisedForm">
                    <textarea id="postContent" name="content" rows="4" cols="10" placeholder="修改朋友圈"></textarea>
                    <div class="word_limit">
                        0/200
                    </div>
                    <select id="visibilityButton" name="visibility">
                        <option value="public">公开</option>
                        <option value="friends">仅好友可见</option>
                        <option value="private">仅自己可见</option>
                    </select>
                    <div class="actions" style="margin-top: 8px;">
                        <button id="revisedButton" class="button">修改</button>
                    </div>
                </form>
            `;
        }
        else if (event.target.id === "revisedButton") {
            event.preventDefault();
            const content = postsContainer.querySelector("#postContent");
            const text = content.value.trim();
            const wordCountDisplay = postsContainer.querySelector(".word_limit");
            const visibility = postsContainer.querySelector("#visibilityButton").value;
            if (!text) {
                alert('内容不能为空');
                return;
            }
            if (text.length > wordLimit) {
                alert(`内容不能超过 ${wordLimit} 字`);
                return;
            }
            try {
                const res = await fetch(`/api/post/${post_id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content: text, visibility: visibility }),
                });
                if (res.ok) {
                    const newPost = await res.json();
                    content.value = '';
                    wordCountDisplay.textContent = `0/${wordLimit}`;
                    wordCountDisplay.style.color = '#6b778c';
                    alert('朋友圈修改成功');
                    myFetch();
                } else {
                    alert('朋友圈修改失败');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('修改朋友圈时发生错误');
            }
        }
        else if (event.target.id === "delete") {
            try {
                const res = await fetch(`/api/post/${post_id}`, { method: 'DELETE' });
                if (res.ok) {
                    alert("删除成功")
                    myFetch();
                } else {
                    alert('删除失败');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('删除时发生错误');
            }
        }
    });


    commentsContainer.addEventListener('click', async (event) => {
        if (event.target.id === "commentButton") {
            event.preventDefault();
            const content = commentsContainer.querySelector("#commentContent");
            const text = content.value.trim();
            const wordCountDisplay = commentsContainer.querySelector(".word_limit");
            if (!text) {
                alert('内容不能为空');
                return;
            }
            if (text.length > wordLimit) {
                alert(`内容不能超过 ${wordLimit} 字`);
                return;
            }
            try {
                const res = await fetch(`/api/comments/${post_id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content: text }),
                });
                if (res.ok) {
                    const newPost = await res.json();
                    content.value = '';
                    wordCountDisplay.textContent = `0/${wordLimit}`;
                    wordCountDisplay.style.color = '#6b778c';
                    alert('评论发布成功');
                    myFetch();
                } else {
                    alert('评论发布失败');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('发布评论时发生错误');
            }
        }
    });

    postsContainer.addEventListener('input', () => {
        const content = postsContainer.querySelector("#postContent");
        const currentLength = content.value.length;
        const wordCountDisplay = postsContainer.querySelector(".word_limit");
        wordCountDisplay.textContent = `${currentLength}/${wordLimit}`;
        if (currentLength > wordLimit) {
            wordCountDisplay.style.color = 'red';
        } else {
            wordCountDisplay.style.color = '#6b778c';
        }
    })


    commentsContainer.addEventListener('input', () => {
        const content = commentsContainer.querySelector("#commentContent");
        const currentLength = content.value.length;
        const wordCountDisplay = commentsContainer.querySelector(".word_limit");
        wordCountDisplay.textContent = `${currentLength}/${wordLimit}`;
        if (currentLength > wordLimit) {
            wordCountDisplay.style.color = 'red';
        } else {
            wordCountDisplay.style.color = '#6b778c';
        }
    })

    myFetch();
});