"""
Error Controller

エラーページを表示するコントローラー
"""

from app.core.AppController import AppController
import flet as ft

class ErrorController(AppController):
    """
    エラーページを表示するコントローラー
    """
    
    def not_found(self):
        """
        404エラーページを表示する
        
        Returns:
            None
        """
        self.set("title", "404 - ページが見つかりません")
        self.set("message", "リクエストされたページが見つかりませんでした。")
        self.set("route", self._request.get_route())
