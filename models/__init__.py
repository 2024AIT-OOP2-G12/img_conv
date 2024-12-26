from peewee import SqliteDatabase
from .db import db
from .history import History


# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    History,
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()