"""
Error Handler Module

このモジュールはエラーハンドリングのためのユーティリティ関数を提供します。
"""

import flet as ft

def handle_404(page, route):
    """
    404エラーページを表示する
    
    Args:
        page: fletのPageオブジェクト
        route: エラーが発生したルート
    """
    controls = [
        ft.Text(
            "404 - ページが見つかりません",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="red"
        ),
        ft.Text(
            f"リクエストされたページ '{route}' は存在しません。",
            size=16
        ),
        ft.Container(
            content=ft.ElevatedButton(
                "ホームに戻る",
                icon=ft.Icons.HOME,
                on_click=lambda _: page.go("/")
            ),
            margin=ft.margin.only(top=20)
        )
    ]
    
    _show_error_page(page, route, controls)

def handle_error(page, route, error_message="エラーが発生しました"):
    """
    一般的なエラーページを表示する
    
    Args:
        page: fletのPageオブジェクト
        route: エラーが発生したルート
        error_message: エラーメッセージ
    """
    controls = [
        ft.Text(
            "エラー",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="red"
        ),
        ft.Text(
            error_message,
            size=16
        ),
        ft.Container(
            content=ft.ElevatedButton(
                "ホームに戻る",
                icon=ft.Icons.HOME,
                on_click=lambda _: page.go("/")
            ),
            margin=ft.margin.only(top=20)
        )
    ]
    
    _show_error_page(page, route, controls)

def _show_error_page(page, route, controls):
    """
    エラーページを表示する
    
    Args:
        page: fletのPageオブジェクト
        route: エラーが発生したルート
        controls: 表示するコントロールのリスト
    """
    page.views.clear()
    page.views.append(
        ft.View(route=route, controls=controls)
    )
    page.update()
