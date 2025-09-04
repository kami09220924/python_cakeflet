"""
AppModel Module

このモジュールはMVCフレームワークの基本となるモデルクラスを定義します。
全てのモデルはこのクラスを継承して使用します。
"""

from peewee import Model, SqliteDatabase
import importlib
import os
from config import app

# データベース接続設定
if app.DATABASE['engine'] == 'sqlite':
    db = SqliteDatabase(app.DATABASE['file'])
else:
    # 他のデータベースエンジンにも対応する場合はここに実装
    db = SqliteDatabase('src/database/fletmvc.db')  # デフォルトはSQLite

class AppModel(Model):
    """
    アプリケーションのベースモデルクラス
    全てのモデルはこのクラスを継承します
    """
    
    class Meta:
        database = db
    
    def __init__(self):
        """
        モデルの初期化
        """
        self._table_name = None
        self._query = None
    
    @property
    def query(self):
        """
        クエリプロパティ
        モデルに対するクエリを開始するためのプロパティ
        
        Returns:
            クエリオブジェクト
        """
        return self.__class__.select()
    
    def find(self, id):
        """
        IDでレコードを検索する
        
        Args:
            id: レコードID
            
        Returns:
            見つかったレコード
        """
        return self.__class__.get_by_id(id)
    
    def find_all(self):
        """
        全てのレコードを取得する
        
        Returns:
            レコードのリスト
        """
        return list(self.__class__.select())
    
    def save_record(self, data):
        """
        レコードを保存する
        
        Args:
            data: 保存するデータの辞書
            
        Returns:
            保存されたレコード
        """
        if 'id' in data and data['id']:
            # 更新
            record = self.__class__.get_by_id(data['id'])
            for key, value in data.items():
                if key != 'id' and hasattr(record, key):
                    setattr(record, key, value)
            record.save()
            return record
        else:
            # 新規作成
            if 'id' in data:
                del data['id']
            record = self.__class__.create(**data)
            return record
    
    def delete_record(self, id):
        """
        レコードを削除する
        
        Args:
            id: 削除するレコードのID
            
        Returns:
            削除が成功したかどうか
        """
        try:
            record = self.__class__.get_by_id(id)
            record.delete_instance()
            return True
        except:
            return False
    
    @classmethod
    def get_all_models(cls):
        """
        全てのモデルクラスを取得する
        
        Returns:
            モデルクラスの辞書 {名前: クラス}
        """
        models = {}
        models_dir = os.path.join('src', 'app', 'models')
        
        if not os.path.exists(models_dir):
            return models
            
        for filename in os.listdir(models_dir):
            if filename.endswith('.py') and filename != '__init__.py' and filename != 'AppModel.py':
                model_name = filename[:-3]  # .pyを除去
                try:
                    module = importlib.import_module(f"app.models.{model_name}")
                    model_class = getattr(module, model_name)
                    if issubclass(model_class, cls):
                        models[model_name] = model_class
                except (ImportError, AttributeError):
                    pass
                    
        return models
