import json
import sys
import time
import urllib2

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
ARMATURE_OUT = 23
GPIO.setup(ARMATURE_OUT, GPIO.OUT)
GPIO.output(ARMATURE_OUT, False)
LAST_CHECKIN = None

while True:
  try:
    checkin = json.loads(urllib2.urlopen(sys.argv[1]).read())
  except urllib2.URLError:
    print 'urllib error'
    raise
    time.sleep(10)
    continue
  id = checkin['id']
  if LAST_CHECKIN == None:
    LAST_CHECKIN = id
    print 'initialized'

  if LAST_CHECKIN != id:
    LAST_CHECKIN = id
    GPIO.output(ARMATURE_OUT, True)
    time.sleep(30)
    GPIO.output(ARMATURE_OUT, False)
    
  time.sleep(3)
