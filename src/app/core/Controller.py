"""
Controller Module

このモジュールはMVCフレームワークのコントローラーファクトリークラスを定義します。
コントローラーの読み込みと実行を管理します。
"""

import importlib
import os
import re
import flet as ft
from app.core.Request import Request
from app.core.Response import Response
from app.core.View import View

class Controller:
    """
    コントローラーを管理するファクトリークラス
    コントローラーの読み込みと実行を担当します
    """
    
    @staticmethod
    def load(controller_name):
        """
        指定された名前のコントローラーをロードする
        
        Args:
            controller_name: コントローラーの名前
            
        Returns:
            コントローラーのインスタンス
        """
        # コントローラー名を正規化
        controller_class_name = Controller._normalize_controller_name(controller_name)
        
        try:
            # コントローラーをインポート
            module_path = f"app.controllers.{controller_class_name}"
            module = importlib.import_module(module_path)
            controller_class = getattr(module, controller_class_name)
            
            # インスタンスを作成して返す
            return controller_class()
        except (ImportError, AttributeError) as e:
            print(f"コントローラーのロードに失敗しました: {e}")
            return None
    
    @staticmethod
    def _normalize_controller_name(name):
        """
        コントローラー名を正規化する
        
        Args:
            name: 元のコントローラー名
            
        Returns:
            正規化されたコントローラークラス名
        """
        # 特殊なコントローラー名の対応
        """ special_cases = {
            "test_list": "TestListController",
            "testlist": "TestListController"
        }
        
        # 特殊なケースを先にチェック
        lower_name = name.lower()
        if lower_name in special_cases:
            return special_cases[lower_name] """

        if (name in "_"):
            # snake_case から CamelCase に変換
            parts = name.split('_')
            camel_case = ''.join(part.capitalize() for part in parts)
        else:
            camel_case = name
        
        # 'Controller' サフィックスがなければ追加
        if not camel_case.endswith('Controller'):
            camel_case += 'Controller'
            
        return camel_case
    
    @staticmethod
    def get_available_controllers():
        """
        利用可能なコントローラーの一覧を取得する
        
        Returns:
            利用可能なコントローラー名のリスト
        """
        controllers = []
        controllers_dir = os.path.join('src', 'app', 'controllers')
        
        if not os.path.exists(controllers_dir):
            return controllers
            
        for filename in os.listdir(controllers_dir):
            if filename.endswith('Controller.py') and filename != '__init__.py':
                controller_name = filename[:-3]  # .pyを除去
                controllers.append(controller_name)
                
        return controllers
    
    @staticmethod
    def execute(page, controller_name, action_name="index", params=None):
        """
        コントローラーのアクションを実行する
        
        Args:
            page: fletのPageオブジェクト
            controller_name: コントローラー名
            action_name: 実行するアクション（メソッド）名
            params: ルートパラメータ
            
        Returns:
            アクションの実行結果
        """
        # パラメータの初期化
        if params is None:
            params = {}

        # コントローラー名からサフィックスを削除
        if controller_name.endswith('Controller'):
            base_controller_name = controller_name[:-10]
        else:
            base_controller_name = controller_name
            
        # コントローラーをロード
        controller = Controller.load(base_controller_name)
        if controller is None:
            from app.core.ErrorHandler import handle_404
            handle_404(page, f"{base_controller_name}:{action_name}")
            return None
            
        # リクエストとレスポンスを作成
        route = f"{base_controller_name}:{action_name}"
        request = Request(page, route, params)
        response = Response(page)
        
        # コントローラーの初期化
        controller.initialize(request, response)
        
        # アクションメソッドの存在確認
        if not hasattr(controller, action_name):
            from app.core.ErrorHandler import handle_404
            handle_404(page, route)
            return None
            
        # アクションの実行
        action_method = getattr(controller, action_name)
        result = action_method()
        
        # ビューをレンダリング
        view = View(base_controller_name, action_name, controller.get_layout())
        controls = view.render(page, controller.get_view_vars())
        
        response.set_controls(controls).render(route)
        
        return result
