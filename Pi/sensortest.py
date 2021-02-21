#!//usr/bin/python3
import os
from os import path
import sys
import time
from datetime import datetime
import json
import board
import busio
import adafruit_gps
import adafruit_bmp3xx
import adafruit_hts221
import adafruit_ltr390
import adafruit_tsl2591
import adafruit_scd30

#last_print = time.monotonic()

i2c = busio.I2C(board.SCL, board.SDA)
bmpJSONFileName = "/home/pi/bmpData.json"
#
# Try GPS Board
#
gps = "noSensor"
try:
    gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface
except:
    gps = "noSensor"

if gps == "noSensor":
    print("GPS Sensor -NOT- Detected")
else:
    print("GPS Sensor Detected")

bmp = "noSensor"
try:
    bmp                          = adafruit_bmp3xx.BMP3XX_I2C(i2c)
except:
    bmp                          = "noSensor"

if bmp == "noSensor":
    print("BMP Sensor -NOT- Detected")
else:
    print("BMP Sensor Detected")

try:
    hts                          = adafruit_hts221.HTS221(i2c)
except:
    hts                          = "noSensor"

if hts == "noSensor":
    print("HTS Sensor -NOT- Detected")
else:
    print("BMP Sensor Detected")

try:
    ltr                          = adafruit_ltr390.LTR390(i2c)
except:
    ltr                          = "noSensor"

if ltr == "noSensor":
    print("LTR Sensor -NOT- Detected")
else:
    print("LTR Sensor Detected")

try:
    tsl                          = adafruit_tsl2591.TSL2591(i2c)
except:
    tsl                          = "noSensor"

if tsl == "noSensor":
    print("TSL Sensor -NOT- Detected")
else:
    print("TSL Sensor Detected")

try:
    scd                          = adafruit_scd30.SCD30(i2c)
except:
    scd                          = "noSensor"

if scd == "noSensor":
    print("SCD Sensor -NOT- Detected")
else:
    print("SCD Sensor Detected")
