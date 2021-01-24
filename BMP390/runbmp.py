#!/usr/bin/env python
'''
  runbmp.py
  Collect Barometric Pressure and Temperature from BMPx8x sensors
  and record them into a log file
  2017-07-27 - Donald Bower
'''
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import time

BASEDIR="/mnt/usbstick/data"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
DATAFILE='$BASEDIR/bmpdata_{:s}.txt'.format(TimeStampStr)

F1 = open(DATAFILE, "w", 1) # Open File, write to disk every line.

def setup():
	print ("Setting up, please wait...")
	print "Open File ", DATAFILE, " for append"

def loop():
	sensor = BMP085.BMP085()

	while True:
		BMPtemp = sensor.read_temperature()	# Read temperature to veriable temp
		BMPpressure = sensor.read_pressure()	# Read pressure to veriable pressure

		if BMPpressure is not None and BMPtemp is not None:
			TimeStampStr = time.strftime("%Y-%m-%d %H:%M:%S")
			BMPTempStr = '|BMP-Temp|{0:=+010.5f} C'.format(BMPtemp)
			BMPPressureStr = '|BMP-Pressure|{0:=+010.5f} Pa'.format(BMPpressure)
			print ("{:s}{:s}{:s}{:s}{:s}".format(TimeStampStr,BMPTempStr,BMPPressureStr))
			F1.write('{:s}{:s}{:s}{:s}{:s}\n'.format(TimeStampStr,BMPTempStr,BMPPressureStr))
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
