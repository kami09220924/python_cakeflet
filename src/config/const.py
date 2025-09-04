class Const:
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError(f"定数 '{name}' は変更できません")
        else:
            raise AttributeError(f"定数は直接セットできません。define()を使用してください。")

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(f"定数 '{name}' は存在しません")

    def define(self, name, value):
        if name in self.__dict__:
            raise AttributeError(f"定数 '{name}' は変更できません")
        else:
            self.__dict__[name] = value

    def defined(self, name):
        return name in self.__dict__


APP_CONST = Const()

""" 
* ここから定数定義
"""
APP_CONST.define("PAGENAME", {
    "テスト一覧": "test_list"
})