import webapp2
from google.appengine.api import users

import jinja2
import os
from contextlib import contextmanager
import urllib
import json

import logging


import config
import usertoken
import lastcheckin

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class ConfigPage(webapp2.RequestHandler):
  def ensure_admin(self):
    user = users.get_current_user()
    if user:
      if users.is_current_user_admin():
        return True
      else:
        self.error(500)
        return False
    else:
      self.redirect(users.create_login_url(self.request.uri))

  def get(self):
    if self.ensure_admin():
      self.render()

  def post(self):
    if self.ensure_admin():
      client_id = self.request.get('client_id')
      client_secret = self.request.get('client_secret')
      callback_url = self.request.get('callback_url')
      config.set_config(client_id, client_secret, callback_url)
      self.render()

  def render(self):
    if config.has_config():
      conf = config.get_config()
      client_id = conf.client_id
      client_secret = conf.client_secret
      callback_url = conf.callback_url
    else:
      client_id = ''
      client_secret = ''
      callback_url = ''

    template_values = {
      'client_id': client_id,
      'client_secret': client_secret,
      'callback_url': callback_url
    }
    template = jinja_environment.get_template('config.html')
    self.response.out.write(template.render(template_values)) 

class LogoutPage(webapp2.RequestHandler):
  def get(self):
      self.redirect(users.create_logout_url('/'))

class MainPage(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'client_id': config.get_config().client_id,
      'redirect_uri': urllib.quote_plus(os.path.join(self.request.uri,'oauth_callback'))
    }
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values)) 

class OAuthCallbackPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      code = self.request.get('code')
      conf = config.get_config()
      params = urllib.urlencode({
        "client_id": conf.client_id,
        "client_secret": conf.client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": conf.callback_url,
        "code": code
      })
      token_json = urllib.urlopen("https://foursquare.com/oauth2/access_token?%s" % params).read()
      try:
        token_obj = json.loads(token_json)
        token = token_obj['access_token']
        usertoken.set(user.user_id(), token)
      except KeyError:
        logging.warn(token_json)
 
    else:
      self.redirect(users.create_login_url(self.request.uri))

class VenuePushPage(webapp2.RequestHandler):
  def post(self):
    logging.info('venue push')
    checkin_json = self.request.get('checkin')
    checkin = json.loads(checkin_json)
    logging.info(self.request.get('checkin'))
    lastcheckin.set(
      checkin['venue']['id'],
      checkin_json)

class VenueDoorPage(webapp2.RequestHandler):
  def get(self, venue_id):
    checkin=lastcheckin.get(venue_id)

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(checkin.checkin)

logging.info('Starting Main handler')
app = webapp2.WSGIApplication([ 
                                ('/', MainPage),
                                ('/logout', LogoutPage),
                                ('/oauth_callback', OAuthCallbackPage),
                                ('/venue_push', VenuePushPage),
                                ('/api/door/([a-fA-F0-9]{24})', VenueDoorPage),
                                ('/config', ConfigPage),
                              ],
                              debug=True)

