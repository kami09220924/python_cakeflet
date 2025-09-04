"""
Main Application Module

アプリケーションのエントリーポイント
"""

import os
import flet as ft
from app.core.Router import Router
from app.core.Controller import Controller
# from auth.authentication import SaltedHashAuth
from config import app

def main(page: ft.Page):
    """
    メイン関数
    
    Args:
        page: fletのPageオブジェクト
    """
    # ルーターを初期化
    router = Router()
    
    # ルート変更ハンドラを設定
    page.on_route_change = lambda e: router.handle_route(page, e.route)
    
    # ページリロード関数を定義
    page.reload = lambda: router.handle_route(page, page.route)
    
    # テーマを設定
    theme_config = app.APP['theme']
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=theme_config.get('color_scheme_seed', 'green')
    )
    
    # 認証を設定
    # page.custom_auth = SaltedHashAuth()
    
    # 初期ルートへ遷移（新しいルーティング形式を使用）
    page.go("Home:index/TestList:index")

if __name__ == "__main__":
    # 環境変数からポートを取得（Herokuなどのデプロイ環境用）
    port = int(os.getenv("PORT", 5000))
    
    # アプリケーションを起動
    ft.app(target=main, port=port)