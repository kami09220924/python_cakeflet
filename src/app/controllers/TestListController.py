"""
Test List Controller

テスト一覧を管理するコントローラー
"""

from app.core.AppController import AppController

class TestListController(AppController):
    """
    テスト一覧を管理するコントローラー
    """
    
    def index(self):
        """
        テスト一覧を表示する
        
        Returns:
            None
        """
        # ビュー変数をセット
        self.set("title", "テスト一覧")
        self.set("tests", ["TEST1", "TEST2", "TEST3"])
        
        # モデルからデータを取得する例
        # user_model = self.load_model("User")
        # users = user_model.find_all()
        # self.set("users", users)
    
    def detail(self):
        """
        テスト詳細を表示する
        
        Returns:
            None
        """
        # ルートパラメータからIDを取得
        test_id = self._request.get_param("id")
        
        # テストデータをセット
        self.set("title", f"テスト詳細 - {test_id}")
        self.set("test_id", test_id)
        self.set("test_name", f"テスト{test_id}")
        self.set("test_description", f"これはテスト{test_id}の説明です。")
    
    def add(self):
        """
        テスト追加フォームを表示する
        
        Returns:
            None
        """
        self.set("title", "テスト追加")
        self.set("form_action", "create")
    
    def create(self):
        """
        テストを作成する
        
        Returns:
            None
        """
        # POSTデータを取得
        # name = self._request.get_data("name")
        
        # テストを作成
        # ここではモデルを使った処理を省略
        
        # 一覧ページにリダイレクト
        self._response.redirect("/test_list")
    
    def edit(self):
        """
        テスト編集フォームを表示する
        
        Returns:
            None
        """
        # ルートパラメータからIDを取得
        test_id = self._request.get_param("id")
        
        self.set("title", f"テスト編集 - {test_id}")
        self.set("test_id", test_id)
        self.set("test_name", f"テスト{test_id}")
        self.set("form_action", "update")
    
    def update(self):
        """
        テストを更新する
        
        Returns:
            None
        """
        # ルートパラメータからIDを取得
        test_id = self._request.get_param("id")
        
        # POSTデータを取得
        # name = self._request.get_data("name")
        
        # テストを更新
        # ここではモデルを使った処理を省略
        
        # 詳細ページにリダイレクト
        self._response.redirect(f"/test_list/detail/{test_id}")
    
    def delete(self):
        """
        テストを削除する
        
        Returns:
            None
        """
        # ルートパラメータからIDを取得
        test_id = self._request.get_param("id")
        
        # テストを削除
        # ここではモデルを使った処理を省略
        
        # 一覧ページにリダイレクト
        self._response.redirect("/test_list")