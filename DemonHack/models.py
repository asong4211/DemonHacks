from peewee import *;
import datetime;

db1 = SqliteDatabase('posts.db')

class Post(Model):
    id = PrimaryKeyField();
    date = DateTimeField(default = datetime.datetime.now);
    title = CharField(unique=True)
    text = TextField()
    category = TextField()

    class Meta:
        database = db1

def initialize_db():
    db1.connect()
    db1.create_tables([Post], safe = True)
