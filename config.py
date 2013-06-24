from google.appengine.ext import db

class Config(db.Model):
  client_id = db.StringProperty()
  client_secret = db.StringProperty()
  callback_url = db.StringProperty()

def get_config():
  return Config.get_by_key_name('singleton')

def set_config(client_id, client_secret, callback_url):
  Config(
      key_name='singleton',
      client_id=client_id,
      client_secret=client_secret,
      callback_url=callback_url).put()

def has_config():
  return get_config() != None
