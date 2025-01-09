from peewee import SqliteDatabase
from .db import db
from .history import History
from .user import User


# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    History,
    User,
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()