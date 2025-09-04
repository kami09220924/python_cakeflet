"""
Home Controller

ホームページを管理するコントローラー
"""

from app.core.AppController import AppController

class HomeController(AppController):
    """
    ホームページを管理するコントローラー
    """
    
    def index(self):
        """
        ホームページを表示する
        
        Returns:
            None
        """
        # ビュー変数をセット
        self.set("title", "ホーム")
        self.set("message", "ようこそ、FletMVCへ！")
        
        # レイアウトを設定
        self.set_layout("default")
