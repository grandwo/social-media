from .init_db import get_connection
from .user_service import *
from .admin_service import *
from .friend_service import *


# 发布post
def create_post(user_id: int, content: str, visibility: str = "public"):
    if visibility not in ["public", "friends", "private"]:
        raise ValueError("Invalid visibility")
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            INSERT INTO posts (user_id, content, visibility) VALUES (%s, %s, %s)
            """,
            (user_id, content, visibility),
        )
        cursor.connection.commit()
    except Exception as e:
        print(f"Database error: {e}")
        raise e
    finally:
        cursor.close()


# 发布comment
def create_comment(user_id: int, post_id: int, content: str):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            INSERT INTO comments (user_id, post_id, content) VALUES (%s, %s, %s)
            """,
            (user_id, post_id, content),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()


# 删除comment
def remove_comment(comment_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            DELETE FROM comments WHERE comment_id = %s
            """,
            (comment_id,),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()


# 获得指定用户的post
def get_somebody_latest_posts(user_id: int, target_user_id: int, role: str = "admin"):
    """返回post_id, content, visibility, updated_at"""
    if role not in ["user", "admin"]:
        raise ValueError("Invalid role")

    print(f"get {target_user_id}'s posts")
    if role == "admin":
        try:
            cursor = get_connection("admin").cursor()
            cursor.execute(
                """
                SELECT post_id, content, visibility, updated_at
                FROM posts
                WHERE user_id = %s
                ORDER BY updated_at DESC
                """,
                (target_user_id,),
            )
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
    elif user_id == target_user_id:
        try:
            cursor = get_connection("user").cursor()
            cursor.execute(
                """
                SELECT post_id, content, visibility, updated_at
                FROM posts
                WHERE user_id = %s
                ORDER BY updated_at DESC
                """,
                (target_user_id,),
            )
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
    elif are_friends(user_id, target_user_id):
        try:
            cursor = get_connection("user").cursor()
            cursor.execute(
                """
                SELECT post_id, content, visibility, updated_at
                FROM posts
                WHERE user_id = %s AND visibility in ("public", "friends")
                ORDER BY updated_at DESC
                """,
                (target_user_id,),
            )
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
    else:
        try:
            cursor = get_connection("user").cursor()
            cursor.execute(
                """
                SELECT post_id, content, visibility, updated_at
                FROM posts
                WHERE user_id = %s AND visibility = "public"
                ORDER BY updated_at DESC
                """,
                (target_user_id,),
            )
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()


# 根据post_id获取post
def get_post_by_id(post_id: int, user_id: int, role: str = "uesr"):
    """返回post_id, user_id, content, visibility, updated_at"""
    if role not in ["user", "admin"]:
        raise ValueError("Invallid role")
    if role == "admin":
        try:
            cursor = get_connection("admin").cursor()
            cursor.execute(
                """
                SELECT post_id, user_id, content, visibility, updated_at
                FROM posts
                WHERE post_id = %s
                """,
                (post_id,),
            )
            return cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            cursor.close()
    else:
        try:
            cursor = get_connection("user").cursor()
            cursor.execute(
                """
                SELECT p.post_id, p.user_id, p.content, p.visibility, p.updated_at
                FROM posts p
                WHERE p.post_id = %s AND (
                    p.visibility = "public" OR p.user_id = %s OR(
                        p.visibility = "friends" AND p.user_id IN (
                            SELECT f.friend_id
                            FROM friends f
                            WHERE f.user_id = %s
                        )
                    )
                )
                """,
                (post_id, user_id, user_id),
            )
            return cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            cursor.close()


# 根据comment_id获取comment
def get_comment_by_id(comment_id: int, user_id: int, role: str = "uesr"):
    """返回comment_id, post_id, user_id, content, created_at"""
    if role not in ["user", "admin"]:
        raise ValueError("Invallid role")
    if role == "admin":
        try:
            cursor = get_connection("admin").cursor()
            cursor.execute(
                """
                SELECT comment_id, post_id, user_id, content, created_at
                FROM comments
                WHERE comment_id = %s
                """,
                (comment_id,),
            )
            return cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            cursor.close()
    else:
        try:
            cursor = get_connection("user").cursor()
            cursor.execute(
                """
                SELECT c.comment_id, c.post_id, c.user_id, c.content, c.created_at
                FROM comments c
                JOIN posts p ON p.post_id = c.post_id
                WHERE c.comment_id = %s AND (
                    p.visibility = "public" OR p.user_id = %s OR c.user_id = %s OR(
                        p.visibility = "friends" AND p.user_id IN (
                            SELECT f.friend_id
                            FROM friends f
                            WHERE f.user_id = %s
                        )
                    )
                )
                """,
                (comment_id, user_id, user_id, user_id),
            )
            return cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            cursor.close()


# 修改post
def update_post(post_id: int, content: str, visibility: str = "public"):
    if visibility not in ["public", "friends", "private"]:
        raise ValueError("Invalid visibility")
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            UPDATE posts SET content = %s, visibility = %s WHERE post_id = %s
            """,
            (content, visibility, post_id),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()


# 删除post
def remove_post(post_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            DELETE FROM posts WHERE post_id = %s
            """,
            (post_id,),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()


# 根据post_id获取comments
def get_comments_by_post_id(post_id: int):
    """返回comment_id, user_id, content, created_at"""
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT comment_id, user_id, content, created_at
            FROM comments
            WHERE post_id = %s
            ORDER BY created_at DESC
            """,
            (post_id,),
        )
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()


# 获得最新好友及自己的post
def get_friends_posts(user_id: int):
    """返回好友及自己的post_id, user_id, content, visibility, updated_at"""
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT p.post_id, p.user_id, p.content, p.visibility, p.updated_at
            FROM posts p
            WHERE p.user_id = %s OR (
                p.visibility IN ('public', 'friends') AND p.user_id IN (
                    SELECT f.friend_id FROM friends f
                    WHERE f.user_id = %s
                )
            )
            ORDER BY p.updated_at DESC
            """,
            (user_id, user_id),
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Database error: {e}")
        raise e
    finally:
        cursor.close()


# 获取所有有权限观看的post
def get_all_posts(user_id: int, role: str = "user"):
    """返回post_id, user_id, content, visibility, updated_at"""
    if role not in ["user", "admin"]:
        raise ValueError("Invalid role")

    if role == "admin":
        try:
            cursor = get_connection("admin").cursor()
            cursor.execute("""
                SELECT p.post_id, p.user_id, p.content, p.visibility, p.updated_at
                FROM posts p
                ORDER BY p.updated_at DESC
                """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            raise e
        finally:
            cursor.close()
    else:
        try:
            cursor = get_connection("user").cursor()
            cursor.execute(
                """
                SELECT p.post_id, p.user_id, p.content, p.visibility, p.updated_at
                FROM posts p
                WHERE p.user_id = %s OR p.visibility = "public" OR (
                    p.visibility = 'friends' AND p.user_id IN (
                        SELECT f.friend_id FROM friends f
                        WHERE f.user_id = %s
                    )
                )
                ORDER BY p.updated_at DESC
                """,
                (user_id, user_id),
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            raise e
        finally:
            cursor.close()
