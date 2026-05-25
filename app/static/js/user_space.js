document.addEventListener('DOMContentLoaded', () => {
    const profileContainer = document.getElementById('profileContainer');
    const role = profileContainer.dataset.role;
    const target_id = profileContainer.dataset.targetId;
    const user_id = profileContainer.dataset.userId;
    let are_friends = profileContainer.dataset.areFriends === 'True';
    async function fetchProfile() {
        console.log('Fetching profile for:', target_id);
        console.log('Current user ID:', user_id);
        console.log('Are friends:', are_friends);
        try {
            const res = await fetch(`/api/user/${target_id}`, { method: 'GET' });
            const target = await res.json();
            console.log('target data:', target);
            if (res.ok) {
                const genderText = target.gender === "male" ? "男" : target.gender === "female" ? "女" : "其他";
                profileContainer.innerHTML = `
                <h1>${target.username} 的个人空间</h1>
                <a href="/posts/${target.user_id}">
                    <h3>${target.username} 的朋友圈</h3>
                </a>
                `
                if (role === "admin") {
                    profileContainer.innerHTML += `
                    <div id="usernameSection">
                        <p>用户名: ${target.username}</p>
                    </div>
                    <div id="dateSection">
                        <p>注册日期: ${new Date(target.created_at).toLocaleString()}</p>
                    </div>
                    <button id="deleteUserBtn">删除用户</button>`;
                }
                else if (target.user_id == user_id) {
                    profileContainer.innerHTML += `
                    <div id="usernameSection">
                        <p>用户名: ${target.username}</p>
                        <button id="editUsernameBtn">修改用户名</button>
                    </div>
                    <div id="genderSection">
                        <p>性别: ${genderText}</p>
                        <button id="editGenderBtn">修改性别</button>
                    </div>
                    <div id="dateofBirthSection">
                        <p>出生日期: ${target.date_of_birth ? new Date(target.date_of_birth).toLocaleDateString() : '未设置'}</p>
                        <button id="editDOBBtn">修改出生日期</button>
                    </div>
                    <div id="passwordSection">
                        <p>密码: ********</p>
                        <button id="editPasswordBtn">修改密码</button>
                    </div>
                    <div id="dateSection">
                        <p>注册日期: ${new Date(target.created_at).toLocaleString()}</p>
                    </div>
                `;
                }
                else if (are_friends) {
                    profileContainer.innerHTML += `
                    <div id="usernameSection">
                        <p>用户名: ${target.username}</p>
                    </div>
                    <div id="genderSection">
                        <p>性别: ${genderText}</p>
                    </div>
                    <div id="dateofBirthSection">
                        <p>出生日期: ${target.date_of_birth ? new Date(target.date_of_birth).toLocaleDateString() : '未设置'}</p>
                    </div>
                    <div id="dateSection">
                        <p>注册日期: ${new Date(target.created_at).toLocaleString()}</p>
                    </div>
                    <button id="deleteFriendBtn">删除好友</button>
                `;
                }
                else {
                    profileContainer.innerHTML += `
                    <div id="usernameSection">
                        <p>用户名: ${target.username}</p>
                    </div>
                    <button id="addFriendBtn">添加好友</button>
                `;
                }
            } else {
                console.error('Failed to load user profile:', res.status);
                profileContainer.innerHTML = '<p>用户信息加载失败。</p>';
            }
        } catch (error) {
            console.error('Error:', error);
            profileContainer.innerHTML = '<p>用户信息加载失败。</p>';
        }
    }

    fetchProfile();

    profileContainer.addEventListener('click', async (event) => {
        let revisedValue = null;
        let field = null;
        if (event.target.id === 'editUsernameBtn') {
            const reviseUsernameSecttion = document.getElementById('usernameSection');
            reviseUsernameSecttion.innerHTML = `
                <input type="text" id="newUsername" placeholder="请输入新用户名">
                <button id="saveUsernameBtn">保存</button>
            `;
        }
        else if (event.target.id === 'editGenderBtn') {
            const reviseGenderSection = document.getElementById('genderSection');
            reviseGenderSection.innerHTML = `
                <select id="newGender">
                    <option value="male">男</option>
                    <option value="female">女</option>
                    <option value="other">其他</option>
                </select>
                <button id="saveGenderBtn">保存</button>
            `;
        }
        else if (event.target.id === 'editDOBBtn') {
            const reviseDOBDSection = document.getElementById('dateofBirthSection');
            reviseDOBDSection.innerHTML = `
                <input type="date" id="newDOBD">
                <button id="saveDOBDBtn">保存</button>
            `;
        }
        else if (event.target.id === 'editPasswordBtn') {
            const revisePasswordSection = document.getElementById('passwordSection');
            revisePasswordSection.innerHTML = `
                <input type="password" id="newPassword" placeholder="请输入新密码">
                <button id="savePasswordBtn">保存</button>
            `;
        }
        else if (event.target.id === 'saveUsernameBtn') {
            const newUsername = document.getElementById('newUsername').value;
            revisedValue = newUsername;
            field = 'username';
        }
        else if (event.target.id === 'saveGenderBtn') {
            const newGender = document.getElementById('newGender').value;
            revisedValue = newGender;
            field = 'gender';
        }
        else if (event.target.id === 'saveDOBDBtn') {
            const newDOBD = document.getElementById('newDOBD').value;
            revisedValue = newDOBD;
            field = 'date_of_birth';
        }
        else if (event.target.id === 'savePasswordBtn') {
            const newPassword = document.getElementById('newPassword').value;
            revisedValue = newPassword;
            field = 'password';
        }
        else if (event.target.id === 'addFriendBtn') {
            try {
                const res = await fetch(`/api/friends`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id1: user_id, id2: target_id }),
                })
                if (res.ok) {
                    alert('好友添加成功')
                    are_friends = true
                    fetchProfile();
                }
                else {
                    alert('好友添加失败')
                    console.error('Failed to add friend')
                }
            }
            catch (error) {
                console.error('Error:', error);
            }
        }
        else if (event.target.id === 'deleteFriendBtn') {
            try {
                const res = await fetch(`/api/friends`, {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id1: user_id, id2: target_id }),
                })
                if (res.ok) {
                    alert('好友删除成功');
                    are_friends = false;
                    fetchProfile();
                }
                else {
                    alert('好友删除失败');
                    console.error('Failed to add friend');
                }
            }
            catch (error) {
                console.error('Error:', error);
            }
        }
        else if (event.target.id === 'deleteUserBtn') {
            try {
                const res = await fetch(`/api/user/${target_id}`, { method: 'DELETE' });
                if (res.ok) {
                    alert('用户删除成功');
                    location.reload();
                }
                else {
                    console.error('Error:', res.error);
                    alert('用户删除失败');
                }
            }
            catch (error) {
                console.error('Error:', error);
            }
        }


        console.log(`Updating field ${field} to ${revisedValue} for user_id ${user_id}`);
        if (revisedValue !== null) {
            if (revisedValue.trim() === '') {
                alert('输入不能为空');
                return;
            }
            if (field === "username") {
                console.log('check whether username exists,', revisedValue);
                try {
                    const res = await fetch(`/api/username/${encodeURIComponent(revisedValue)}`, { method: 'GET' });
                    if (res.ok) {
                        if (res !== null) {
                            alert(`用户名已存在`);
                            return;
                        }
                    }
                    else {
                        console.error('Failed to load user profile by username:', res.status);
                    }
                }
                catch (error) {
                    console.error('Error:', error);
                }
            }
            try {
                const res = await fetch(`/api/user/${user_id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ field: field, value: revisedValue })
                });
                const data = await res.json();
                if (res.ok) {
                    console.log('Profile updated successfully:', data);
                    fetchProfile();
                } else {
                    console.error('Failed to update profile:', data.error);
                }
            } catch (error) {
                console.error('Error updating profile:', error);
            }
        }
    });
});