document.addEventListener('DOMContentLoaded', () => {
    const groupsContainer = document.getElementById('groupsContainer');
    const user_id = groupsContainer.dataset.userId;

    async function fetchGroups() {
        try {
            const res = await fetch(`/api/friend_groups`, { method: 'GET' });
            if (res.ok) {
                const groups = await res.json();
                console.log("groups:", groups);
                groupsContainer.innerHTML = '';
                if (groups.length === 0) {
                    groupsContainer.innerHTML = '<p>无好友分组</p>';
                }
                else {
                    for (const group of groups) {
                        groupsContainer.innerHTML += `
                            <div class="group">
                                <a href="/friend_group/${group.group_id}" target="_blank">
                                    <h3>${group.group_name}</h3>
                                </a>
                                <span class="timestamp">创建于 ${new Date(group.created_at).toLocaleString()}</span>
                            </div>
                        `;
                    }
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

    const createGroupSection = document.getElementById('createGroupSection');

    createGroupSection.addEventListener('click', async (event) => {
        if (event.target.id === "createGroupButton") {
            event.preventDefault()
            createGroupSection.innerHTML = `
                <input type="text" id="newGroupName" placeholder="请输入组名">
                <button id="saveBtn">保存</button>
            `;
        }
        else if (event.target.id === "saveBtn") {
            const group_name = document.getElementById('newGroupName').value;
            try {
                const res = await fetch('/api/friend_groups', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ group_name: group_name }),
                });
                if (res.ok) {
                    alert('分组创建成功');
                    createGroupSection.innerHTML = `
                        <button id = "createGroupButton">创建分组</button>
                        `;
                    fetchGroups();
                } else {
                    console.error('Error:', res.error);
                    alert('分组创建失败');
                }
            }
            catch (error) {
                console.error('Error:', error);
                alert('创建分组时发生错误');
            }

        }
    });

    fetchGroups()

});