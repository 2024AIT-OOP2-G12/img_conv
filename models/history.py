from peewee import Model,DateTimeField, BlobField, CharField, ForeignKeyField
from .db import db
from .user import User

class History(Model):
    user = ForeignKeyField(User, backref='histories')
    times = DateTimeField()  # 変換日時
    image_data = BlobField(null=True)  # 画像データ（Base64エンコード）

    class Meta:
        database = db