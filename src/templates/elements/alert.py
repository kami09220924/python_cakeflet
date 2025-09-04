"""
Alert Element

アラートメッセージを表示するエレメント
"""

import flet as ft

def main(message, type="info", dismissable=True, **kwargs):
    """
    アラートメッセージを表示するエレメント
    
    Args:
        message: 表示するメッセージ
        type: アラートタイプ (info, success, warning, error)
        dismissable: 閉じるボタンを表示するかどうか
        **kwargs: その他のパラメータ
        
    Returns:
        アラートコントロール
    """
    # タイプに応じた色を設定
    colors = {
        "info": "blue",
        "success": "green",
        "warning": "orange",
        "error": "red"
    }
    bg_color = colors.get(type, "blue")
    
    # アラートを作成
    alert = ft.Container(
        content=ft.Row(
            [
                ft.Icon(
                    name=ft.Icons.INFO if type == "info" else 
                          ft.Icons.CHECK_CIRCLE if type == "success" else
                          ft.Icons.WARNING if type == "warning" else
                          ft.Icons.ERROR,
                    color="white"
                ),
                ft.Text(
                    message,
                    color="white",
                    size=14,
                    weight=ft.FontWeight.W500,
                    expand=True
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color="white",
                    icon_size=16,
                    visible=dismissable,
                    on_click=lambda e: e.control.parent.parent.visible = False
                ) if dismissable else ft.Container(width=0)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor=bg_color,
        border_radius=5,
        padding=10,
        margin=ft.margin.only(bottom=10)
    )
    
    return alert
