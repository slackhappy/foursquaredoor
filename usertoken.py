from google.appengine.ext import db

class UserToken(db.Model):
  token = db.StringProperty()

def get(user_id):
  return UserToken.get_by_key_name(user_id)

def set(user_id, token):
  UserToken(key_name=user_id, token=token).put()
