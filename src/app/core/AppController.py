"""
AppController Module

このモジュールはMVCフレームワークの基本となるコントローラークラスを定義します。
全てのコントローラーはこのクラスを継承して使用します。
"""

import flet as ft
from app.core.Request import Request

class AppController:
    """
    アプリケーションのベースコントローラークラス
    全てのコントローラーはこのクラスを継承します
    """
    
    def __init__(self):
        self._view_vars = {}
        self._layout = "default"
        self._elements = {}
        self._name = self.__class__.__name__.replace('Controller', '').lower()
        self._request = None
        self._response = None
        self._models = {}
    
    def initialize(self, request, response):
        """
        コントローラーの初期化処理
        """
        self._request = request
        self._response = response
        return self
    
    def set(self, var_name, value):
        """
        ビューに渡す変数をセットする
        CakePHPの$this->set()と同様の機能
        """
        self._view_vars[var_name] = value
        return self
    
    def get_view_vars(self):
        """
        ビュー変数を取得する
        """
        return self._view_vars
    
    def set_layout(self, layout_name):
        """
        使用するレイアウトをセットする
        """
        self._layout = layout_name
        return self
    
    def get_layout(self):
        """
        現在のレイアウト名を取得する
        """
        return self._layout
    
    def load_model(self, model_name):
        """
        モデルをロードする
        """
        if model_name in self._models:
            return self._models[model_name]
            
        try:
            import importlib
            module_path = f"app.models.{model_name}"
            module = importlib.import_module(module_path)
            model_class = getattr(module, model_name)
            model_instance = model_class()
            self._models[model_name] = model_instance
            return model_instance
        except Exception as e:
            print(f"モデルのロードに失敗しました: {e}")
            return None
    
    def load_component(self, component_name, **params):
        """
        コンポーネント（エレメント）をロードする
        """
        try:
            import importlib
            module_path = f"templates.components.{component_name}"
            module = importlib.import_module(module_path)
            if hasattr(module, "main"):
                return module.main(**params)
            else:
                print(f"コンポーネント '{component_name}' に main 関数がありません")
                return []
        except Exception as e:
            print(f"コンポーネントのロードに失敗しました: {e}")
            return []
