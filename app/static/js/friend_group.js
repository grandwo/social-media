document.addEventListener('DOMContentLoaded', () => {
    const groupsContainer = document.getElementById('groupsContainer');
    const group_id = groupsContainer.dataset.groupId;

    async function fetchGroup() {
        try {
            const res = await fetch(`/api/friend_group/${group_id}`, { method: 'GET' });
            if (res.ok) {
                const group = await res.json();
                console.log("group:", group);
                groupsContainer.innerHTML = '';
                if (!group) {
                    groupsContainer.innerHTML = '<p>无法查看该好友分组</p>';
                }
                else {
                    groupsContainer.innerHTML += `
                        <div class="group">
                            <h3>${group.group_name}</h3>
                            <span class="timestamp">创建于 ${new Date(group.created_at).toLocaleString()}</span>
                        </div>
                        <div id="deleteGroupSection">
                            <button id = "deleteGroupButton">删除分组</button>
                        </div>
                        <div id="addFriendSection">
                            <button id = "addFriendButton">添加好友</button>
                        </div>
                        <div id="friendsContainer" style="margin-top: 16px;"></div>
                    `;
                }
            }
            else {
                console.error("Error:", error);
                groupsContainer.innerHTML = '<p>好友分组加载失败。</p>';
            }
        }
        catch (error) {
            console.error("Error:", error);
            groupsContainer.innerHTML = '<p>好友分组加载失败。</p>';
        }
    }

    groupsContainer.addEventListener('click', async (event) => {
        if (event.target.id === "deleteGroupButton") {
            try {
                const res = await fetch(`/api/friend_group/${group_id}`, { method: 'DELETE' });
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
        if (event.target.id === "addFriendButton") {
            const addFriendSection = document.getElementById("addFriendSection");
            try {
                const res1 = await fetch(`/api/friends`, { method: 'GET' });
                const res2 = await fetch(`/api/friends/friend_group/${group_id}`, { method: 'GET' })
                if (res1.ok & res2.ok) {
                    const list1 = await res1.json();
                    const list2 = await res2.json();
                    const friends = list1.filter(a => !list2.some(b => b.user_id === a.user_id));
                    let html = `
                        <select id="friendSelect">
                    `;
                    for (const friend of friends) {
                        html += `
                            <option value="${friend.user_id}">${friend.username}</option>
                        `;
                    }
                    html += `
                        </select>
                        <button id="addFriend">确认</button>
                    `;
                    addFriendSection.innerHTML = html;
                }
                else {
                    alert('获取好友时出现错误')
                }
            }
            catch (error) {
                console.error('Error:', error);
                alert('获取好友时出现错误');
            }
        }
        if (event.target.id === "addFriend") {
            const friend_id = document.getElementById("friendSelect").value;
            try {
                const res = await fetch(`/api/friend_group/${group_id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ friend_id: friend_id }),
                });
                if (res.ok) {
                    alert('好友添加成功');
                    myFetch();
                } else {
                    console.error('Error:', res.error);
                    alert('好友添加失败');
                }
            }
            catch (error) {
                console.error('Error:', error);
                alert('添加好友时出现错误');
            }
        }
    });



    async function fetchFriends() {
        const friendsContainer = document.getElementById('friendsContainer');
        if (friendsContainer) {
            try {
                const res = await fetch(`/api/friends/friend_group/${group_id}`, { method: 'GET' });
                if (res.ok) {
                    const friends = await res.json();
                    console.log("friends:", friends);
                    friendsContainer.innerHTML = '';
                    if (friends.length === 0) {
                        friendsContainer.innerHTML = '<p>无好友</p>';
                    }
                    else {
                        for (const friend of friends) {
                            friendsContainer.innerHTML += `
                                <div class="friend">
                                    <a href="/user/${friend.user_id}" target="_blank">
                                        <h3>${friend.username}</h3>
                                    </a>
                                    <span class="timestamp">添加于 ${new Date(friend.added_at).toLocaleString()}</span>
                                </div>
                            `;
                        }
                    }
                }
                else {
                    console.error("Error:", error);
                    friendsContainer.innerHTML = '<p>好友加载失败。</p>';
                }
            }
            catch (error) {
                console.error("Error:", error);
                friendsContainer.innerHTML = '<p>好友加载失败。</p>';
            }
        }
    }

    async function myFetch() {
        await fetchGroup();
        await fetchFriends();
    }

    myFetch();
});