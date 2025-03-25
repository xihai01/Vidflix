from mongoengine import Document, StringField, ListField

class User(Document):
  _id = StringField(primary_key=True)
  username = StringField(required=True, unique=True)
  email = StringField(required=True, unique=True)
  password = StringField(required=True)
  image = StringField(default='')
  search_history = ListField()
