import pymysql

from config import ROOT_DB_CONFIG, DB_CONFIGS

import os


# 初始化数据库连接配置
def init_database():
    # 获取当前文件所在目录，并构建SQL文件路径
    current_dir = os.path.dirname(__file__)
    sql_path = os.path.join(current_dir, "create_table.sql")

    # 使用 ROOT_DB_CONFIG（超级用户）来创建数据库和表
    db_config = ROOT_DB_CONFIG.copy()
    db_config.pop("database", None)

    with open(sql_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # 尝试连接数据库并执行SQL文件中的语句，如果连接或执行失败会抛出异常
    try:
        cursor = pymysql.connect(**db_config).cursor()

        # 分割SQL文件内容为单独的语句，并执行每条语句
        statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

        for statement in statements:
            if statement:
                print(f"Executing: {statement[:50]}...")
                cursor.execute(statement)

        cursor.connection.commit()
        print("Database and tables initialized successfully!")
    except pymysql.Error as e:
        print(f"Error initializing database: {e}")
        raise e
    finally:
        cursor.close()

# 获取数据库连接
def get_connection(role: str = "user") -> pymysql.connections.Connection:
    """根据角色返回数据库连接。role 可选值：'user' 或 'admin'。"""
    try:
        cfg = DB_CONFIGS.get(role)
        if cfg is None:
            raise ValueError(f"Unknown DB role: {role}")
        return pymysql.connect(**cfg)
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        raise e


if __name__ == "__main__":
    print("Initializing database...")
    try:
        init_database()
    except Exception as e:
        print(f"An error occurred: {e}")
