from .init_db import get_connection
from .user_service import *

# 添加好友
def add_friend(user_id: int, friend_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            INSERT INTO friends (user_id, friend_id) VALUES (%s, %s), (%s, %s)
            """,
            (user_id, friend_id, friend_id, user_id))
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 删除好友
def remove_friend(user_id: int, friend_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            DELETE FROM friends WHERE user_id = %s AND friend_id = %s
            """,
            (user_id, friend_id))
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 新建好友分组
def create_friend_group(user_id: int, group_name: str):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            INSERT INTO friend_groups (user_id, group_name) VALUES (%s, %s)
            """,
            (user_id, group_name),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 删除好友分组
def remove_friend_group(group_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            DELETE FROM friend_groups WHERE group_id = %s
            """,
            (group_id,),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 将好友添加到分组
def add_friend_to_group(group_id: int, friend_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            INSERT INTO friend_group_members (group_id, friend_id) VALUES (%s, %s)
            """,
            (group_id, friend_id),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 将好友从分组移除
def remove_friend_from_group(group_id: int, friend_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            DELETE FROM friend_group_members WHERE group_id = %s AND friend_id = %s
            """,
            (group_id, friend_id),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 检查两个用户是否是好友
def are_friends(user_id: int, friend_id: int) -> bool:
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT 1 FROM friends WHERE user_id = %s AND friend_id = %s
            """,
            (user_id, friend_id),
        )
        return cursor.fetchone() is not None
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 获取所有好友
def get_friends(user_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT friend_id, created_at FROM friends WHERE user_id = %s
            """,
            (user_id),
        )
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 通过user_id获取friend_groups
def get_friend_groups_by_user_id(user_id: int):
    '''返回group_id, group_name, created_at'''
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT group_id, group_name, created_at
            FROM friend_groups
            WHERE user_id = %s
            """,
            (user_id,),
        )
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 通过group_id获取friend_group
def get_friend_group_by_id(group_id: int, user_id: int, role: str="user"):
    '''返回user_id, group_name, created_at'''
    if role not in ["user", "admin"]:
        raise ValueError("Invalid role")

    if role == "admin":
        try:
            cursor = get_connection("admin").cursor()
            cursor.execute(
                """
                SELECT user_id, group_name, created_at
                FROM friend_groups
                WHERE group_id = %s
                """,
                (group_id,),
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
                SELECT user_id, group_name, created_at
                FROM friend_groups
                WHERE group_id = %s AND user_id = %s
                """,
                (group_id, user_id),
            )
            return cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            cursor.close()

# 通过group_id获取friends
def get_friends_by_group_id(group_id: int):
    '''返回friend_id, added_at'''
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT friend_id, added_at
            FROM friend_group_members
            WHERE group_id = %s
            """,
            (group_id,),
        )
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()