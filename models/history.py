from peewee import Model,DateTimeField, BlobField
from .db import db

class History(Model):
    times = DateTimeField()  # 変換日時
    image_data = BlobField(null=True)  # 画像データ（Base64エンコード）

    class Meta:
        database = db