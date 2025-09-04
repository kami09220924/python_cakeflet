"""
User Model

ユーザー情報を管理するモデル
"""

from peewee import CharField, BooleanField
from app.models.AppModel import AppModel

class User(AppModel):
    """
    ユーザーモデル
    """
    username = CharField(unique=True)
    password = CharField()
    salt = CharField()
    is_active = BooleanField(default=True)
    
    def __init__(self):
        super().__init__()
        self._table_name = "users"
    
    def validate_password(self, password, salt=None):
        """
        パスワードを検証する
        
        Args:
            password: 検証するパスワード
            salt: ソルト（省略可）
            
        Returns:
            検証結果（True/False）
        """
        # パスワード検証ロジックをここに実装
        # 実際にはハッシュ化やソルト処理を行う
        return password == self.password
    
    def find_by_username(self, username):
        """
        ユーザー名でユーザーを検索する
        
        Args:
            username: ユーザー名
            
        Returns:
            ユーザーオブジェクト
        """
        return self.query.where(User.username == username).first()
