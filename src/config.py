# 仅用于初始化数据库
ROOT_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',     #修改为自己的数据库root密码
    'database': 'social_media',
    'charset': 'utf8mb4'
}

# 应用运行时使用的数据库账号（按角色分配）。
DB_CONFIGS = {
    'user': {
        'host': 'localhost',
        'user': 'app_user',
        'password': '0123456789',
        'database': 'social_media',
        'charset': 'utf8mb4'
    },
    'admin': {
        'host': 'localhost',
        'user': 'app_admin',
        'password': '9876543210',
        'database': 'social_media',
        'charset': 'utf8mb4'
    }
}