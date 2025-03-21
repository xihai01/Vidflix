from mongoengine import Document, StringField, ImageField, ListField

class User(Document):
  username = StringField(required=True, unique=True)
  email = StringField(required=True, unique=True)
  password = StringField(required=True)
  image = StringField(default='')
  search_history = ListField()
