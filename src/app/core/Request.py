"""
Request Module

このモジュールはHTTPリクエストを表現するクラスを定義します。
CakePHPのServerRequestに相当します。
"""

class Request:
    """
    HTTPリクエストを表すクラス
    ルートパラメータ、クエリパラメータ、POSTデータなどを管理します
    """
    
    def __init__(self, page, route, params=None):
        """
        Requestオブジェクトの初期化
        
        Args:
            page: flet.Pageオブジェクト
            route: 現在のルート
            params: ルートから抽出されたパラメータ
        """
        self._page = page
        self._route = route
        self._params = params or {}
        self._query_params = {}
        self._post_data = {}
        
        # クエリパラメータの解析
        if '?' in route:
            route_part, query_part = route.split('?', 1)
            self._parse_query_params(query_part)
    
    def _parse_query_params(self, query_string):
        """
        クエリ文字列を解析してパラメータに変換する
        
        Args:
            query_string: クエリ文字列 (例: "param1=value1&param2=value2")
        """
        if not query_string:
            return
            
        params = query_string.split('&')
        for param in params:
            if '=' in param:
                key, value = param.split('=', 1)
                self._query_params[key] = value
            else:
                self._query_params[param] = True
    
    def get_param(self, name, default=None):
        """
        ルートパラメータを取得する
        
        Args:
            name: パラメータ名
            default: パラメータが存在しない場合のデフォルト値
            
        Returns:
            パラメータの値またはデフォルト値
        """
        return self._params.get(name, default)
    
    def get_query(self, name, default=None):
        """
        クエリパラメータを取得する
        
        Args:
            name: パラメータ名
            default: パラメータが存在しない場合のデフォルト値
            
        Returns:
            パラメータの値またはデフォルト値
        """
        return self._query_params.get(name, default)
    
    def get_data(self, name, default=None):
        """
        POSTデータを取得する
        
        Args:
            name: データ名
            default: データが存在しない場合のデフォルト値
            
        Returns:
            データの値またはデフォルト値
        """
        return self._post_data.get(name, default)
    
    def get_route(self):
        """
        現在のルートを取得する
        
        Returns:
            現在のルート文字列
        """
        return self._route
    
    def get_page(self):
        """
        現在のPageオブジェクトを取得する
        
        Returns:
            flet.Pageオブジェクト
        """
        return self._page
    
    def set_post_data(self, data):
        """
        POSTデータをセットする
        
        Args:
            data: POSTデータの辞書
        """
        self._post_data = data
        return self
