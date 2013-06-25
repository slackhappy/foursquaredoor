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

A basic implementation of this is provided in the client directory.

On your Pi:

    sudo pip install RPi.GPIO
    sudo python client/door.py https://YOUR.APP.appspot.com/api/door/VENUE.ID


Here is a rough schematic:

![Buzzer Schematic](http://cl.ly/image/2A0v0g401E3P/Screen%20Shot%202013-06-24%20at%2011.42.08%20PM.png)

Note that door.py uses pin #23:

![GPIO Model B Pinout](http://elinux.org/images/2/2a/GPIOs.png)

And parts list:

- [large solenoid](http://www.adafruit.com/products/413)
- [power supply for solenoid](http://www.adafruit.com/products/352)
- [power supply adapter](http://www.adafruit.com/products/373)
- [TIP120 darlington transistor](http://www.adafruit.com/products/976)
- [1N4001 diode](http://www.adafruit.com/products/755)
- [resistors](http://www.radioshack.com/product/index.jsp?productId=2062304)
