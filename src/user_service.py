from .init_db import get_connection

# 创建用户
def create_user(username: str, password: str, gender: str, date_of_birth: str = None):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            INSERT INTO users (username, password, gender, date_of_birth)
            VALUES (%s, %s, %s, %s)
            """,
            (
                username,
                password,
                gender,
                date_of_birth,
            ),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 删除用户
def remove_user(user_id: int):
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            DELETE FROM users WHERE user_id = %s
            """,
            (user_id,),
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 根据用户id获取用户信息
def get_user_by_id(user_id: int):
    '''返回user_id, username, password, created_at, gender, date_of_birth'''
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT * FROM users WHERE user_id = %s
            """,
            (user_id,),
        )
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 根据用户名获取用户信息
def get_user_by_username(username: str):
    '''返回user_id, username, password, created_at, gender, date_of_birth'''
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT * FROM users WHERE username = %s
            """,
            (username,),
        )
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 修改用户信息
def update_user_field(user_id: int, field: str, value: str):
    if field not in ["username", "password", "gender", "date_of_birth"]:
        raise ValueError("Invalid field")
    try:
        cursor = get_connection("user").cursor()
        print(f"Updating user_id {user_id}: setting {field} to {value}")
        cursor.execute(
            f"""
            UPDATE users SET {field} = %s WHERE user_id = %s
            """,
            (value, user_id)
        )
        cursor.connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()

# 获取所有用户ID
def get_all_users_id():
    '''返回user_id'''
    try:
        cursor = get_connection("user").cursor()
        cursor.execute(
            """
            SELECT user_id FROM users
            """
        )
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
