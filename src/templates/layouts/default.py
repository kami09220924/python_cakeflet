"""
Default Layout

アプリケーションのデフォルトレイアウトを定義します。
"""

import flet as ft
from templates.components.basic import header, breadcrumbs

def main(page, content, title="FletMVC", **kwargs):
    """
    デフォルトレイアウトをレンダリングします
    
    Args:
        page: fletのPageオブジェクト
        content: コンテンツコントロールのリスト
        title: ページタイトル
        **kwargs: その他のパラメータ
        
    Returns:
        レイアウトが適用されたコントロールのリスト
    """
    return [
        header(page=page, title=title),
        breadcrumbs(page=page),
        ft.Container(
            content=ft.Column(
                controls=content,
                spacing=10,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=10,
            expand=True
        )
    ]
