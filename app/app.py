from flask import Flask, jsonify, request, render_template, session, redirect, url_for

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.user_service import *
from src.admin_service import *
from src.post_service import *
from src.friend_service import *

app = Flask(__name__)
app.secret_key = "你自己的随机秘钥"


@app.before_request
def require_admin_for_admin_paths():
    if request.path.startswith("/admin") or request.path.startswith("/api/admin"):
        if not session.get("logged_in") or session.get("role") != "admin":
            if request.path.startswith("/api/"):
                return jsonify({"error": "权限不足"}), 403
            return redirect(url_for("login"))


@app.route("/")
def index():
    return render_template(
        "index.html",
        logged_in=session.get("logged_in", False),
        username=session.get("username"),
        role=session.get("role"),
    )


# 获取所有有权限观看的post
@app.route("/api/all_posts", methods=["GET"])
def get_all_posts_endpoint():
    try:
        posts = get_all_posts(session.get("id"), session.get("role"))
        posts_list = [
            {
                "post_id": post[0],
                "user_id": post[1],
                "content": post[2],
                "visibility": post[3],
                "updated_at": post[4].isoformat(),
                "username": get_user_by_id(post[1])[1],
            }
            for post in posts
        ]
        return jsonify(posts_list), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 注册
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/api/register", methods=["POST"])
def create_user_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    try:
        create_user(
            data["username"],
            data["password"],
            data["gender"],
            data.get("date_of_birth"),
        )
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 登录
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_endpoint():
    data = request.get_json()
    if not data:
        print("Received invalid JSON data")
        return jsonify({"error": "Invalid JSON data"}), 400

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        print("Username or password missing in request data")
        return jsonify({"error": "用户名和密码必须填写"}), 400

    try:
        user = get_user_by_username(username)
        if not user:
            print("User not found")
            return jsonify({"error": "用户不存在"}), 404
        elif user and user[2] == password:
            session["logged_in"] = True
            session["id"] = user[0]
            session["username"] = username
            session["role"] = "user"
        else:
            print("Invalid username or password")
            return jsonify({"error": "密码错误"}), 401
        return (
            jsonify(
                {"message": "登录成功", "username": user[1], "role": session["role"]}
            ),
            200,
        )
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 管理员登录
@app.route("/login/admin")
def admin_login():
    return render_template("login_admin.html")


@app.route("/login/admin", methods=["POST"])
def admin_login_endpoint():
    data = request.get_json()
    if not data:
        print("Received invalid JSON data")
        return jsonify({"error": "Invalid JSON data"}), 400

    admin_id = data.get("admin_id")
    password = data.get("password")
    if not admin_id or not password:
        print("Admin ID or password missing in request data")
        return jsonify({"error": "管理员id和密码必须填写"}), 400

    try:
        admin = get_admin_by_id(admin_id)
        print("admin数据：", admin)
        if not admin:
            print("Admin not found")
            return jsonify({"error": "管理员不存在"}), 404
        elif admin and admin[1] == password:
            print(f"Admin {admin_id} logged in successfully")
            session["logged_in"] = True
            session["id"] = admin_id
            session["role"] = "admin"
        else:
            print("Invalid admin_id or password")
            return jsonify({"error": "密码错误"}), 401
        return (
            jsonify(
                {
                    "message": "管理员登录成功",
                    "admin_id": admin[0],
                    "role": session["role"],
                }
            ),
            200,
        )
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 登出
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# 获取所有用户
@app.route("/users")
def all_users():
    return render_template(
        "users.html",
        logged_in=session.get("logged_in", False),
        user_id=session.get("id"),
        role=session.get("role"),
    )


@app.route("/api/users", methods=["GET"])
def get_all_users_endpoint():
    try:
        users_id = get_all_users_id()
        users_list = [
            {"user_id": user_id, "username": get_user_by_id(user_id)[1]}
            for user_id in users_id
        ]
        return jsonify(users_list), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 个人空间
@app.route("/user/<int:user_id>")
def user_space(user_id):
    return render_template(
        "user_space.html",
        logged_in=session.get("logged_in", False),
        user_id=session.get("id"),
        role=session.get("role"),
        exist_id=get_user_by_id(user_id) is not None,
        target_id=user_id,
        are_friends=(
            are_friends(session.get("id"), user_id)
            if session.get("logged_in") and session.get("role") == "user"
            else False
        ),
    )


@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user_by_id_endpoint(user_id):
    try:
        user = get_user_by_id(user_id)
        if user:
            user_dict = {
                "user_id": user[0],
                "username": user[1],
                "password": user[2],
                "created_at": user[3].isoformat(),
                "gender": user[4],
                "date_of_birth": user[5].isoformat() if user[5] else None,
            }
            return jsonify(user_dict), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    field = data.get("field")
    value = data.get("value")

    if not field or value is None:
        return jsonify({"error": "Invalid field or value"}), 400

    try:
        update_user_field(user_id, field, value)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/user/<int:user_id>", methods=["DELETE"])
def remove_user_endpoint(user_id):
    try:
        remove_user(user_id)
        return jsonify({"message": "用户删除成功"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    


@app.route("/api/username/<username>", methods=["GET"])
def get_user_by_username_endpoint(username):
    try:
        user = get_user_by_username(username)
        if user:
            user_dict = {
                "user_id": user[0],
                "username": user[1],
                "password": user[2],
                "created_at": user[3].isoformat(),
                "gender": user[4],
                "date_of_birth": user[5].isoformat() if user[5] else None,
            }
            return jsonify(user_dict), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 好友列表
@app.route("/friends")
def friends():
    return render_template(
        "friends.html",
        logged_in=session.get("logged_in", False),
        user_id=session.get("id"),
        role=session.get("role"),
    )


@app.route("/api/friends", methods=["GET"])
def get_friends_endpoint():
    try:
        friends = get_friends(session.get("id"))
        friends_list = [
            {
                "user_id": friend[0],
                "username": get_user_by_id(friend[0])[1],
                "created_at": friend[1].isoformat(),
            }
            for friend in friends
        ]
        return jsonify(friends_list), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 添加好友
@app.route("/api/friends", methods=["POST"])
def add_friend_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    id1 = data.get("id1")
    id2 = data.get("id2")

    if get_user_by_id(id1) is None or get_user_by_id(id2) is None:
        return jsonify({"error": "User not Found"}), 404

    try:
        add_friend(id1, id2)
        return jsonify({"message": "好友添加成功"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 删除好友
@app.route("/api/friends", methods=["DELETE"])
def remove_friend_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    id1 = data.get("id1")
    id2 = data.get("id2")

    if get_user_by_id(id1) is None or get_user_by_id(id2) is None:
        return jsonify({"error": "User not Found"}), 404

    try:
        remove_friend(id1, id2)
        return jsonify({"message": "好友删除成功"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 好友分组
@app.route("/friend_groups")
def friend_groups():
    return render_template(
        "friend_groups.html",
        logged_in=session.get("logged_in", False),
        user_id=session.get("id"),
        role=session.get("role"),
    )


@app.route("/api/friend_groups", methods=["GET"])
def get_friend_groups_endpoint():
    try:
        groups = get_friend_groups_by_user_id(session.get("id"))
        groups_list = [
            {
                "group_id": group[0],
                "group_name": group[1],
                "created_at": group[2].isoformat(),
            }
            for group in groups
        ]
        return jsonify(groups_list), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 创建好友分组
@app.route("/api/friend_groups", methods=["POST"])
def create_friend_group_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    try:
        create_friend_group(session.get("id"), data.get("group_name"))
        return jsonify({"message": "Group created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 单个好友分组
@app.route("/friend_group/<int:group_id>")
def friend_group(group_id):
    return render_template(
        "friend_group.html",
        logged_in=session.get("logged_in", False),
        user_id=session.get("id"),
        role=session.get("role"),
        group_id=group_id,
    )


@app.route("/api/friend_group/<int:group_id>", methods=["GET"])
def get_friend_group_by_id_endpoint(group_id):
    try:
        group = get_friend_group_by_id(group_id, session.get("id"), session.get("role"))
        if group is None:
            return jsonify(group), 200
        group_dict = {
            "user_id": group[0],
            "group_name": group[1],
            "created_at": group[2].isoformat(),
            "username": get_user_by_id(group[0])[1],
        }
        return jsonify(group_dict), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 删除好友分组
@app.route("/api/friend_group/<int:group_id>", methods=["DELETE"])
def remove_friend_group_endpoint(group_id):
    try:
        remove_friend_group(group_id)
        return jsonify({"message": "删除成功"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 根据group_id获取好友
@app.route("/api/friends/friend_group/<int:group_id>", methods=["GET"])
def get_friends_by_group_id_endpoint(group_id):
    try:
        friends = get_friends_by_group_id(group_id)
        friends_list = [
            {
                "user_id": friend[0],
                "username": get_user_by_id(friend[0])[1],
                "added_at": friend[1].isoformat(),
            }
            for friend in friends
        ]
        return jsonify(friends_list), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 将好友加入分组
@app.route("/api/friend_group/<int:group_id>", methods=["POST"])
def add_friend_to_group_endpoint(group_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    try:
        add_friend_to_group(group_id, data.get("friend_id"))
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 用户朋友圈界面
@app.route("/posts/<int:user_id>")
def user_posts(user_id):
    return render_template(
        "user_posts.html",
        logged_in=session.get("logged_in", False),
        user_id=session.get("id"),
        role=session.get("role"),
        exist_id=get_user_by_id(user_id) is not None,
        target_id=user_id,
    )


@app.route("/api/posts/<int:user_id>", methods=["GET"])
def get_posts_by_id_endpoint(user_id):
    try:
        posts = get_somebody_latest_posts(
            session.get("id"), user_id, session.get("role")
        )
        username = get_user_by_id(user_id)[1]
        posts_list = [
            {
                "post_id": post[0],
                "content": post[1],
                "visibility": post[2],
                "updated_at": post[3].isoformat(),
            }
            for post in posts
        ]
        ret_dict = {
            "posts_list": posts_list,
            "username": username,
        }
        return jsonify(ret_dict), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/posts/<int:user_id>", methods=["POST"])
def create_post_endpoint(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    try:
        create_post(user_id, data["content"], data["visibility"])
        return jsonify({"message": "Post created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 单条朋友圈界面
@app.route("/post/<int:post_id>")
def post(post_id):
    return render_template(
        "post.html",
        logged_in=session.get("logged_in", False),
        user_id=session.get("id"),
        role=session.get("role"),
        post_id=post_id,
    )


@app.route("/api/post/<int:post_id>", methods=["GET"])
def get_post_by_id_endpoint(post_id):
    try:
        post = get_post_by_id(post_id, session.get("id"), session.get("role"))
        if post is None:
            return jsonify(None), 200
        post_dict = {
            "post_id": post[0],
            "user_id": post[1],
            "content": post[2],
            "visibility": post[3],
            "updated_at": post[4].isoformat(),
            "username": get_user_by_id(post[1])[1],
        }
        return jsonify(post_dict), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 修改朋友圈
@app.route("/api/post/<int:post_id>", methods=["PUT"])
def update_post_endpoint(post_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    content = data.get("content")
    visibility = data.get("visibility")

    try:
        update_post(post_id, content, visibility)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 删除朋友圈
@app.route("/api/post/<int:post_id>", methods=["DELETE"])
def remove_post_endpoint(post_id):
    try:
        remove_post(post_id)
        return jsonify({"message": "删除成功"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 根据post_id获取评论
@app.route("/api/comments/<int:post_id>", methods=["GET"])
def get_comments_by_post_id_endpoint(post_id):
    try:
        comments = get_comments_by_post_id(post_id)
        comments_list = [
            {
                "comment_id": comment[0],
                "user_id": comment[1],
                "username": get_user_by_id(comment[1])[1],
                "content": comment[2],
                "created_at": comment[3].isoformat(),
            }
            for comment in comments
        ]
        return jsonify(comments_list), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 创建评论
@app.route("/api/comments/<int:post_id>", methods=["POST"])
def create_comment_endpoint(post_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    content = data.get("content")
    try:
        create_comment(session.get("id"), post_id, content)
        return jsonify({"message": "comment created successfully"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 单条评论
@app.route("/comment/<int:comment_id>")
def comment(comment_id):
    return render_template(
        "comment.html",
        logged_in=session.get("logged_in", False),
        user_id=session.get("id"),
        role=session.get("role"),
        comment_id=comment_id,
    )


# 根据 comment_id 获取评论
@app.route("/api/comment/<int:comment_id>", methods=["GET"])
def get_comment_by_comment_id_endpoint(comment_id):
    try:
        comment = get_comment_by_id(comment_id, session.get("id"), session.get("role"))
        if comment is None:
            return jsonify(None), 200
        comment_dict = {
            "comment_id": comment[0],
            "post_id": comment[1],
            "user_id": comment[2],
            "content": comment[3],
            "created_at": comment[4].isoformat(),
            "username": get_user_by_id(comment[2])[1],
        }
        return jsonify(comment_dict), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 删除评论
@app.route("/api/comment/<int:comment_id>", methods=["DELETE"])
def remove_comment_endpoint(comment_id):
    try:
        remove_comment(comment_id)
        return jsonify({"message": "删除成功"}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500


# 查看自己及好友的朋友圈
@app.route("/posts")
def posts():
    return render_template(
        "posts.html",
        logged_in=session.get("logged_in", False),
        username=session.get("username"),
        role=session.get("role"),
    )


@app.route("/api/posts", methods=["GET"])
def get_friends_posts_endpoint():
    try:
        posts = get_friends_posts(session.get("id"))
        posts_list = [
            {
                "post_id": post[0],
                "user_id": post[1],
                "content": post[2],
                "visibility": post[3],
                "updated_at": post[4].isoformat(),
                "username": get_user_by_id(post[1])[1],
            }
            for post in posts
        ]
        return jsonify(posts_list), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
