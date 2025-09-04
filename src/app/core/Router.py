"""
Router Module

このモジュールはURLルーティングを管理するクラスを定義します。
"""

import re
import flet as ft
from app.core.Controller import Controller
from app.core.Request import Request
from app.core.Response import Response
from config import app

class Router:
    """
    URLルーティングを管理するクラス
    """
    
    def __init__(self):
        """
        Routerオブジェクトの初期化
        """
        self._routes = {}
        self._route_tree = {}
        self._default_routes = {
            "/": {
                "controller": app.APP.get('default_controller', 'Home'),
                "action": app.APP.get('default_action', 'index')
            }
        }
        
        # 設定からルートを読み込む
        if hasattr(app, 'ROUTES'):
            self._custom_routes = app.ROUTES
        else:
            self._custom_routes = {}
    
    def add_route(self, pattern, controller, action="index"):
        """
        ルートを追加する
        
        Args:
            pattern: URLパターン
            controller: コントローラー名
            action: アクション名
        """
        self._routes[pattern] = {
            "controller": controller,
            "action": action
        }
    
    def build_route_tree(self):
        """
        ルートツリーを構築する
        """
        # コントローラーリストからルートを自動生成
        controllers = Controller.get_available_controllers()
        
        for controller_name in controllers:
            # コントローラー名からベース名を取得（Controllerサフィックスを除く）
            base_name = controller_name.replace('Controller', '')
            controller_path = f"/{base_name.lower()}"
            
            # コントローラーをロード
            controller = Controller.load(base_name)
            if controller is None:
                continue
                
            # コントローラーのアクションを探す
            for attr_name in dir(controller):
                # プライベートメソッドとデフォルトメソッドはスキップ
                if attr_name.startswith('_') or attr_name in ['initialize', 'set', 'get_view_vars', 'set_layout', 'get_layout', 'load_model', 'load_component']:
                    continue
                    
                # アクション名がindexの場合は特別処理
                if attr_name == 'index':
                    self.add_route(controller_path, base_name, 'index')
                else:
                    action_path = f"{controller_path}/{attr_name}"
                    self.add_route(action_path, base_name, attr_name)
        
        # カスタムルートを追加
        for pattern, route_info in self._custom_routes.items():
            self.add_route(pattern, route_info['controller'], route_info.get('action', 'index'))
            
        # デフォルトルートを追加
        for pattern, route_info in self._default_routes.items():
            if pattern not in self._routes:
                self.add_route(pattern, route_info['controller'], route_info['action'])
                
        # ルートツリーを構築
        for pattern, route_info in self._routes.items():
            parts = pattern.strip('/').split('/')
            current = self._route_tree
            
            for i, part in enumerate(parts):
                if part not in current:
                    current[part] = {}
                
                if i == len(parts) - 1:  # 最後の部分
                    current[part]['__route__'] = {
                        "controller": route_info['controller'],
                        "action": route_info['action']
                    }
                
                current = current[part]
    
    def match(self, route):
        """
        ルートをマッチングする
        
        Args:
            route: URLルート
            
        Returns:
            マッチしたルート情報またはNone
        """
        # クエリパラメータを分離
        if '?' in route:
            route_part, _ = route.split('?', 1)
        else:
            route_part = route
            
        # 末尾のスラッシュを削除
        route_part = route_part.rstrip('/')
        
        # ルートが空の場合はルートパスとして扱う
        if not route_part:
            route_part = '/'
            
        # 完全一致ルートをチェック
        if route_part in self._routes:
            return {
                "controller": self._routes[route_part]["controller"],
                "action": self._routes[route_part]["action"],
                "params": {}
            }
        
        # パターンマッチングルートをチェック
        for pattern, route_info in self._routes.items():
            regex_pattern = self._convert_route_to_regex(pattern)
            match = re.match(f"^{regex_pattern}$", route_part)
            if match:
                return {
                    "controller": route_info["controller"],
                    "action": route_info["action"],
                    "params": match.groupdict()
                }
                
        # 階層的なルートをチェック
        parts = route_part.strip('/').split('/')
        result = self._match_hierarchical(parts, self._route_tree)
        if result:
            return result
            
        # マッチしなかった場合
        return None
    
    def _match_hierarchical(self, parts, tree, params=None):
        """
        階層的なルートをマッチングする（再帰的）
        
        Args:
            parts: URLパーツのリスト
            tree: 現在のツリーノード
            params: パラメータ辞書
            
        Returns:
            マッチしたルート情報またはNone
        """
        if params is None:
            params = {}
            
        if not parts:
            # パスの終端に達した
            if '__route__' in tree:
                return {
                    "controller": tree['__route__']["controller"],
                    "action": tree['__route__']["action"],
                    "params": params
                }
            return None
            
        part = parts[0]
        rest = parts[1:]
        
        # 直接マッチ
        if part in tree:
            result = self._match_hierarchical(rest, tree[part], params)
            if result:
                return result
                
        # パラメータマッチ
        for key in tree:
            if key.startswith('<') and key.endswith('>'):
                # パラメータ名を抽出
                param_name = key[1:-1]
                params[param_name] = part
                
                result = self._match_hierarchical(rest, tree[key], params)
                if result:
                    return result
                    
                # マッチしなかった場合はパラメータを削除
                del params[param_name]
                
        return None
    
    def _convert_route_to_regex(self, route):
        """
        ルートパターンを正規表現に変換する
        
        Args:
            route: ルートパターン
            
        Returns:
            正規表現パターン
        """
        return re.sub(r"<([^>]+)>", r"(?P<\1>[^/]+)", route)
    
    def handle_route(self, page, route):
        """
        ルートをハンドリングする
        
        Args:
            page: fletのPageオブジェクト
            route: URLルート (Controller:View/Controller:View形式またはURLルート形式)
        """
        # ルートツリーが空の場合は構築
        if not self._route_tree:
            self.build_route_tree()
        
        # コントローラー:ビュー形式のルートをパースする
        if ':' in route:
            parts = route.strip('/').split('/')
            routes = []
            params = {}
            
            for part in parts:
                if ':' in part:
                    controller_view = part.split(':')
                    if len(controller_view) == 2:
                        controller_name = controller_view[0]
                        view_name = controller_view[1]
                        
                        # コントローラーとビューが存在するか確認
                        controller = Controller.load(controller_name)
                        if controller is not None and hasattr(controller, view_name):
                            routes.append({
                                "controller": controller_name,
                                "action": view_name,
                                "params": {}
                            })
                        else:
                            # 404エラー - コントローラーまたはビューが見つからない
                            self._handle_404(page, route)
                            return
            
            if routes:
                # 最後のルートを処理する
                route_info = routes[-1]
                Controller.execute(page, route_info["controller"], route_info["action"], route_info["params"])
                return
        else:
            # 従来のURLルートパターンでマッチング
            match_result = self.match(route)
            
            if match_result:
                # コントローラーとアクションを取得
                controller_name = match_result["controller"]
                action_name = match_result["action"]
                params = match_result["params"]
                
                # コントローラーを実行
                Controller.execute(page, controller_name, action_name, params)
                return
                
        # マッチングに失敗した場合は404エラー
        self._handle_404(page, route)
    
    def _handle_404(self, page, route):
        """
        404エラーを表示する
        
        Args:
            page: fletのPageオブジェクト
            route: URLルート
        """
        # エラーハンドラーを使用
        from app.core.ErrorHandler import handle_404
        handle_404(page, route)
