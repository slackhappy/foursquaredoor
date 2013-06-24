# Foursquare Door #

Foursquare Door is a [Push API](https://developer.foursquare.com/overview/realtime) notification holder for google appengine.

## Deploy and Configure ##

- Upload to appengine
- Configure the app (/config)
- Start receving pings for the venues you own

https://YOUR.APP.appspot.com/api/door/VENUE.ID will store the latest checkin


## Uses ##

Use a RaspberryPi to check your door every second for changes.
If your friend checks in, raise a pin connected to a relay that
powers a solenoid that buzzes your friend in!
