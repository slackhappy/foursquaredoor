from google.appengine.ext import db

#key_name = venue
class LastCheckin(db.Model):
  checkin = db.TextProperty()

def get(venue_id):
  return LastCheckin.get_by_key_name(venue_id)

def set(venue_id, checkin):
  LastCheckin(key_name=venue_id, checkin=checkin).put()
