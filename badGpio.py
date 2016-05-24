import picamera
import time
import datetime
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
switchPin = 17
ledPin = 8

# Setup pins
GPIO.setup(switchPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)

# Setup camera
camera = picamera.PiCamera()
camera.resolution = (1024, 768)
save_path = '/home/pi/picamera/' #edit this

# Detect button press
while True:
	GPIO.output(ledPin, GPIO.LOW)
	if(GPIO.input(switchPin)):
		GPIO.output(ledPin, GPIO.HIGH)
		print "Button pressed, three (3) sec to take photo"
		time.sleep(3)
		camera.capture(save_path + 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg')
		#os.system("python /home/pi/run.py") # Run another script
		time.sleep(1)


# For continuous capturing
"""with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(5)
    for filename in camera.capture_continuous(save_path + 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
        print('Captured %s' % filename)
        time.sleep(5)"""