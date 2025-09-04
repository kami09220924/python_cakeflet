"""
Error View

エラーページを表示するビュー
"""

import flet as ft

def main(page, title="エラー", message="エラーが発生しました", route="", **kwargs):
    """
    エラーページを表示する
    
    Args:
        page: fletのPageオブジェクト
        title: エラータイトル
        message: エラーメッセージ
        route: エラーが発生したルート
        **kwargs: その他のパラメータ
        
    Returns:
        エラーページのコントロールリスト
    """
    return [
        ft.Text(
            title,
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED
        ),
        ft.Text(
            message,
            size=16
        ),
        ft.Text(
            f"ルート: {route}",
            size=14,
            color=ft.Colors.GREY
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
