"""
Application Configuration

このモジュールはアプリケーションの設定を定義します。
CakePHPのapp.phpに相当します。
"""

# データベース設定
DATABASE = {
    'engine': 'sqlite',
    'file': 'src/database/fletmvc.db'
}

# アプリケーション設定
APP = {
    'name': 'FletMVC',
    'debug': True,
    'default_layout': 'default',
    'default_controller': 'Home',
    'default_action': 'index',
    'theme': {
        'color_scheme_seed': 'green',
        'theme_mode': 'light'
    }
}

# セッション設定
SESSION = {
    'cookie_name': 'flet_session',
    'lifetime': 86400,  # 1日
    'secure': False,
    'httponly': True
}

# セキュリティ設定
SECURITY = {
    'salt': 'change_this_to_a_random_string',
    'csrf_protection': True,
    'csrf_expires': 3600  # 1時間
}

# メール設定
EMAIL = {
    'default': {
        'transport': 'smtp',
        'host': 'localhost',
        'port': 25,
        'username': '',
        'password': '',
        'tls': False
    }
}

# ログ設定
LOGGING = {
    'level': 'debug',  # debug, info, warning, error, critical
    'file': 'logs/app.log',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# キャッシュ設定
CACHE = {
    'default': {
        'engine': 'file',
        'path': 'tmp/cache/',
        'duration': 3600  # 1時間
    }
}

# 利用可能なアプリは動的に検出されるため、APPS定数は不要になりました

# ルーティング設定（上書き用）
ROUTES = {
    # '/custom/route': {'controller': 'CustomController', 'action': 'customAction'},
}
