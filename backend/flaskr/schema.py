from mongoengine import Document, StringField

class User(Document):
  username = StringField(max_length=50)
  email = StringField(required=True, unique=True)
  password = StringField(max_length=50)
