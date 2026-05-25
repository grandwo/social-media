from .init_db import get_connection

def get_admin_by_id(admin_id: int):
    try:
        cursor = get_connection("admin").cursor()
        cursor.execute(
            """
            SELECT * FROM admins WHERE admin_id = %s
            """,
            (admin_id,),
        )
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()


def update_admin_field(id, field, value):
    try:
        cursor = get_connection("admin").cursor()
        if field not in ["username", "password"]:
            raise ValueError("Invalid field for admin")
        cursor.execute(
            f"""
            UPDATE admins SET {field} = %s WHERE admin_id = %s
            """,
            (value, id),
        )
        cursor.connection.commit()
    except Exception as e:
        print(f"Database error: {e}")
        raise e
    finally:
        if 'cursor' in locals():
            cursor.close()