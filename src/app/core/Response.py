"""
Response Module

このモジュールはHTTPレスポンスを表現するクラスを定義します。
CakePHPのResponseに相当します。
"""

import flet as ft

class Response:
    """
    HTTPレスポンスを表すクラス
    ビューのレンダリングやリダイレクトなどを管理します
    """
    
    def __init__(self, page):
        """
        Responseオブジェクトの初期化
        
        Args:
            page: flet.Pageオブジェクト
        """
        self._page = page
        self._status_code = 200
        self._headers = {}
        self._body = None
        self._controls = []
    
    def set_status(self, code):
        """
        ステータスコードをセットする
        
        Args:
            code: HTTPステータスコード
        """
        self._status_code = code
        return self
    
    def set_header(self, name, value):
        """
        レスポンスヘッダーをセットする
        
        Args:
            name: ヘッダー名
            value: ヘッダー値
        """
        self._headers[name] = value
        return self
    
    def set_controls(self, controls):
        """
        表示するコントロールをセットする
        
        Args:
            controls: fletコントロールのリスト
        """
        self._controls = controls
        return self
    
    def redirect(self, url):
        """
        指定されたURLにリダイレクトする
        
        Args:
            url: リダイレクト先URL
        """
        self._page.go(url)
        return self
    
    def render(self, route):
        """
        現在のコントロールをレンダリングする
        
        Args:
            route: 現在のルート
        """
        self._page.views.clear()
        self._page.views.append(
            ft.View(route=route, controls=self._controls)
        )
        self._page.update()
        return self
