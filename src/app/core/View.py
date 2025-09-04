"""
View Module

このモジュールはMVCフレームワークのビュークラスを定義します。
ビューのレンダリングとテンプレートの管理を担当します。
"""

import importlib
import os
import flet as ft

class View:
    """
    ビューを管理するクラス
    ビューのレンダリングとテンプレートの管理を担当します
    """
    
    def __init__(self, controller_name, action_name, layout_name="default"):
        """
        Viewオブジェクトの初期化
        
        Args:
            controller_name: コントローラー名
            action_name: アクション名
            layout_name: レイアウト名
        """
        self._controller_name = controller_name.lower()
        self._action_name = action_name
        self._layout_name = layout_name
        self._elements = {}
    
    def render(self, page, view_vars):
        """
        ビューをレンダリングする
        
        Args:
            page: fletのPageオブジェクト
            view_vars: ビュー変数の辞書
            
        Returns:
            fletコントロールのリスト
        """
        try:
            # テンプレートのパスを決定
            template_path = self._get_template_path()
            
            # テンプレートをロード
            template = self._load_template(template_path)
            if template is None:
                return [ft.Text("テンプレートが見つかりません")]
            
            # テンプレートにページとビュー変数を渡してレンダリング
            content_controls = self._render_template(template, page, view_vars)
            
            # レイアウトがある場合はレイアウトを適用
            if self._layout_name != "none":
                return self._apply_layout(page, content_controls, view_vars)
            else:
                return content_controls
                
        except Exception as e:
            print(f"ビューのレンダリングに失敗しました: {e}")
            return [ft.Text(f"ビューのレンダリングに失敗しました: {e}")]
    
    def _get_template_path(self):
        """
        テンプレートのパスを取得する
        
        Returns:
            テンプレートのパス
        """
        # コントローラー名とアクション名から適切なテンプレートパスを取得
        # コントローラー名からControllerを除去し小文字に変換
        controller_part = self._controller_name.lower().replace('controller', '')
        
        # アクション名
        action_part = self._action_name.lower()
        
        # テンプレートファイル名（コントローラー名/アクション名）
        template_file = f"{controller_part}.{action_part}"
        
        return template_file
    
    def _load_template(self, template_path):
        """
        テンプレートをロードする
        
        Args:
            template_path: テンプレートのパス
            
        Returns:
            テンプレートモジュール
        """
        try:
            module_path = f"templates.components.{template_path}"
            module = importlib.import_module(module_path)
            return module
        except ImportError:
            print(f"テンプレート '{template_path}' のロードに失敗しました")
            return None
    
    def _render_template(self, template, page, view_vars):
        """
        テンプレートをレンダリングする
        
        Args:
            template: テンプレートモジュール
            page: fletのPageオブジェクト
            view_vars: ビュー変数の辞書
            
        Returns:
            fletコントロールのリスト
        """
        # mainメソッドがあればそれを呼び出す
        if hasattr(template, "main"):
            controls = template.main(page=page, **view_vars)
            if isinstance(controls, list):
                return controls
            else:
                return [controls]
        else:
            # mainメソッドがない場合はエラーを表示
            return [ft.Text(f"テンプレート '{template.__name__}' に main 関数がありません")]
    
    def _apply_layout(self, page, content_controls, view_vars):
        """
        レイアウトを適用する
        
        Args:
            page: fletのPageオブジェクト
            content_controls: コンテンツのコントロールリスト
            view_vars: ビュー変数の辞書
            
        Returns:
            レイアウトが適用されたコントロールのリスト
        """
        try:
            # レイアウトモジュールをロード
            layout_path = f"templates.layouts.{self._layout_name}"
            layout_module = importlib.import_module(layout_path)
            
            # レイアウトのmainメソッドを呼び出す
            if hasattr(layout_module, "main"):
                # コンテンツをビュー変数に追加
                view_vars["content"] = content_controls
                return layout_module.main(page=page, **view_vars)
            else:
                print(f"レイアウト '{self._layout_name}' に main 関数がありません")
                return content_controls
                
        except ImportError as e:
            print(f"レイアウト '{self._layout_name}' のロードに失敗しました")
            print(f"エラー: {e}")
            return content_controls
    
    def element(self, element_name, **params):
        """
        エレメント（部分テンプレート）をロードする
        
        Args:
            element_name: エレメント名
            **params: エレメントに渡すパラメータ
            
        Returns:
            エレメントのコントロールリスト
        """
        try:
            # エレメントをキャッシュから取得するか、ロードする
            if element_name in self._elements:
                element = self._elements[element_name]
            else:
                module_path = f"templates.elements.{element_name}"
                element = importlib.import_module(module_path)
                self._elements[element_name] = element
            
            # エレメントのmainメソッドを呼び出す
            if hasattr(element, "main"):
                return element.main(**params)
            else:
                print(f"エレメント '{element_name}' に main 関数がありません")
                return []
                
        except ImportError:
            print(f"エレメント '{element_name}' のロードに失敗しました")
            return []
