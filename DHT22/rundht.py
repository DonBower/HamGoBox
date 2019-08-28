#!/usr/bin/env python
'''
rundht.py
Collect Humidity, Temperature from DHT-22 sensor
and record them into a log file
2016-07-27 - Donald Bower
'''
import Adafruit_DHT as DHT
import RPi.GPIO as GPIO
import time

DHTSensor = 22
DHTGPIOPin = 21

BASEDIR="/mnt/usbstick/data"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
DATAFILE='$BASEDIR/dhtdata_{:s}.txt'.format(TimeStampStr)

F1 = open(DATAFILE, "w", 1) # Open File, write to disk every line.

def setup():
	print ("Setting up, please wait...")
	print "Open File ", DATAFILE, " for append"

def loop():

	while True:
		DHThumidity, DHTtemp = DHT.read_retry(DHTSensor, DHTGPIOPin)

		if DHThumidity is not None and DHTtemp is not None:
			TimeStampStr = time.strftime("%Y-%m-%d %H:%M:%S")
			DHTTempStr = '|DHT-Temp|{0:=+010.5f} C'.format(DHTtemp)
			DHTHumidityStr = '|DHT-Humidity|{0:=+010.5f}%'.format(DHThumidity)
			print ("{:s}{:s}{:s}{:s}{:s}".format(TimeStampStr,DHTTempStr,DHTHumidityStr))
			F1.write('{:s}{:s}{:s}{:s}{:s}\n'.format(TimeStampStr,DHTTempStr,DHTHumidityStr))
		else:
			print ("'Failed to get reading. Try again!'")
		time.sleep(5)

def destroy():
	GPIO.cleanup()
	F1.close()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
