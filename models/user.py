from peewee import Model, CharField
from .db import db

class User(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db