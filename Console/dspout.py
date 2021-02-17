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
    hasGPS = False
else:
    hasGPS = True
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0") # We only want GGA and RMC sentances...
    gps.send_command(b"PMTK220,1000") # Set Update rate to 1 second

print("GPS Sensor Present: " + str(hasGPS))

bmp = "noSensor"
try:
    bmp                          = adafruit_bmp3xx.BMP3XX_I2C(i2c)
except:
    bmp                          = "noSensor"

if bmp == "noSensor":
    hasBMP                       = False
else:
    hasBMP                       = True
    bmp.pressure_oversampling    = 8
    bmp.temperature_oversampling = 2
    firstHPA                     = 0
    previousMin                  = ""

print("BMP3XX Sensor Present: " + str(hasBMP))

try:
    hts                          = adafruit_hts221.HTS221(i2c)
except:
    hts                          = "noSensor"

if hts == "noSensor":
    hasHTS                       = False
else:
    hasHTS                       = True
    bmp.pressure_oversampling    = 8
    bmp.temperature_oversampling = 2

print("HTS221 Sensor Present: " + str(hasHTS))

try:
    ltr                          = adafruit_ltr390.LTR390(i2c)
except:
    ltr                          = "noSensor"

if ltr == "noSensor":
    hasLTR                       = False
else:
    hasLTR                       = True
    ltr.gain                     = 1
    ltr.resolution               = 4
    ltr.measurement_delay        = 2

print("LTR390 Sensor Present: " + str(hasLTR))

try:
    tsl                          = adafruit_tsl2591.TSL2591(i2c)
except:
    tsl                          = "noSensor"

if tsl == "noSensor":
    hasTSL                       = False
else:
    hasTSL                       = True
    # You can optionally change the gain and integration time:
    # tsl.gain = adafruit_tsl2591.GAIN_LOW (1x gain)
    # tsl.gain = adafruit_tsl2591.GAIN_MED (25x gain, the default)
    # tsl.gain = adafruit_tsl2591.GAIN_HIGH (428x gain)
    # tsl.gain = adafruit_tsl2591.GAIN_MAX (9876x gain)
    # tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS (100ms, default)
    # tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS (200ms)
    # tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS (300ms)
    # tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS (400ms)
    # tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS (500ms)
    # tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS (600ms)

print("TSL2591 Sensor Present: " + str(hasTSL))

try:
    scd                          = adafruit_scd30.SCD30(i2c)
except:
    scd                          = "noSensor"

if scd == "noSensor":
    hasSCD                       = False
else:
    hasSCD                       = True
    thisCO2                      = 0.0

print("SCD30 Sensor Present: " + str(hasSCD))

#f = open('/dev/tty1','w')
#sys.stdout = f

#
# Clear the Screen
#
#os.system("echo clear > /dev/tty1")
def clearScreen():
    print(chr(27) + "[2J")
#
# Print Timestamp
#
def printTimeStamp():
    now = datetime.now()
    timeStampNow = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Timestamp..........: " + timeStampNow)
#
# Print GPS Latitude, Longitude and Maidenhead
#
def getMaidenHead(latitude, longitude):
    maxMaiden  = 4
    A          = ord('A')
    a          = divmod(longitude + 180,20)
    b          = divmod(latitude + 90,10)
    maidenHead = chr(A + int(a[0])) + chr(A + int(b[0]))
    longitude  = a[1]/2
    latitude   = b[1]
    i          = 1
    while i    < maxMaiden:
        i                   += 1
        a                    = divmod(longitude,1)
        b                    = divmod(latitude,1)
        if not(i%2):
            maidenHead      += str(int(a[0]))+str(int(b[0]))
            longitude        = 24*a[1]
            latitude         = 24*b[1]
        else:
            tmp              = i+1
            tmpString        = chr(A+int(a[0]))+chr(A+int(b[0]))
            # Every other set is lowercase
            if not(tmp%4):
                maidenHead  += tmpString.lower()
            else:
                maidenHead  += tmpString
            longitude        = 10*a[1]
            latitude         = 10*b[1]
    return maidenHead

def printGPS():
    gps.update()
#    current = time.monotonic()
#    if current - last_print >= 0.50:
#    last_print = current
    thisLat = gps.latitude
    thisLon = gps.longitude
    thisAltM = gps.altitude_m
    thisSatCount = gps.satellites
    if not isinstance(thisLat, float):
        thisLat = 0.0
    if not isinstance(thisLon, float):
        thisLon = 0.0
    if not isinstance(thisAltM, float):
        thisAltM = 0.0
        thisAltF = 0.0
    else:
        thisAltF = thisAltM * 3.28084
    if not isinstance(thisSatCount, int):
        thisSatCount = 0
    print(f'Maidenhead.........: {getMaidenHead(thisLat, thisLon):8s}                   '[:40])
    print(f'Lat/Lon ({thisSatCount:02d}).......: {thisLat:07.4f} / {thisLon:08.4f}                   '[:40])
    print(f'Altitude...........: {thisAltM:5,.1f}M / {thisAltF:3,.0f}F                   '[:40])

def printBMP():
    global firstHPA, previousMin, haveFullMinute
    now = datetime.now()
    thisMin = now.strftime("%H:%M")
    thisDate = now.strftime("%Y-%m-%d")

    if path.exists(bmpJSONFileName):
        with open(bmpJSONFileName, "r") as jsonFile:
            try:
                bmpJSON = json.load(jsonFile)
            except:
                bmpJSON = None

            if bmpJSON is None:
                bmpJSON = json.loads('{}')

            if thisMin in bmpJSON:
                thisMinData = bmpJSON.get(thisMin)
            else:
                thisMinData = json.loads('{}')
                thisMinData['Date'] = thisDate
                thisMinData['HPATotal'] = 0
                thisMinData['Samples'] = 0
                thisMinData['Trend'] = '→'
    else:
        bmpJSON = json.loads('{}')
        thisMinData = json.loads('{}')
        thisMinData['Date'] = thisDate
        thisMinData['HPATotal'] = 0
        thisMinData['Samples'] = 0
        thisMinData['Trend'] = '→'

    thisMinHPA = thisMinData['HPATotal']
    samplesCount = thisMinData['Samples']
    jsonDate = thisMinData['Date']

    thisHPA = bmp.pressure
#
# Need a 12 hour clock to check if thisMinData is old
#   (because of wraparound or multiday idle)
#   - jsonDate + thisMin > 12 hours thisDate + thisMin is ok.
#
    if thisMin == previousMin:
        samplesCount = samplesCount + 1
        thisMinHPA = thisMinHPA + thisHPA
        minuteAvgHPA = thisMinHPA / samplesCount
    else:
        if samplesCount <= 60:
            haveFullMinute = False
        else:
            haveFullMinute = True
        samplesCount = 1
        thisMinHPA = thisHPA
        minuteAvgHPA = thisHPA
        previousMin = thisMin

    if firstHPA == 0 or not haveFullMinute:
        firstHPA = minuteAvgHPA

    if thisHPA > firstHPA:
        thisHPATrend = '↑'
    else:
        if thisHPA < firstHPA:
            thisHPATrend = '↓'
        else:
            thisHPATrend = '→'

    thisMinData['HPATotal'] = thisMinHPA
    thisMinData['Samples'] = samplesCount
    thisMinData['Trend'] = thisHPATrend
    thisMinData['Date'] = thisDate
    bmpJSON[thisMin] = thisMinData

    with open(bmpJSONFileName, "w") as jsonFile:
        json.dump(bmpJSON, jsonFile, indent=4)

    thisHG = thisHPA / 33.864
    print(f'Barometer hPa/Hg..{thisHPATrend:1s}: {thisHPA:5,.1f} / {thisHG:5.2f}                   '[:40])

def printHTS():
    thisHumidity = hts.relative_humidity
    thisTempC    = hts.temperature
    thisTempF    = ((9.0 / 5.0) * thisTempC + 32)
    print(f'Temperature........: {thisTempC:4.1f}°c /{thisTempF:5.1f}°f                   '[:40])
    print(f'Relative Humidity..: {thisHumidity:4.1f}% rH                   '[:40])

def printLTR():
    thisUV           = ltr.uvs
    thisUVi          = int(round(thisUV / 95), 0)
    thisAmbient      = ltr.light
    print(f'UVa EMF / UVI......: {thisUV:1,d}um/cm^2 / {thisUV:1,d}UVi                   '[:40])
    print(f'Ambient Light......: {thisAmbient:1,d}                   '[:40])

def printTSL():
    thisIR           = tsl.infrared
    thisVis          = tsl.visible
    thisLux          = tsl.lux
    thisFullSpectrum = tsl.full_spectrum
    print(f'Visable Light......: {thisVis:4,d}                   '[:40])
    print(f'Infrared Light.....: {thisIR:1,d}                   '[:40])

def printSCD():
    global thisCO2
    if scd.data_available:
        thisCO2      = scd.CO2
    print(f'CO2................: {thisCO2:4,.1f}ppm                   '[:40])

clearScreen()
while True:
#    sys.stdout.write("\x1b[2J\x1b[H") # Position to top
    sys.stdout.write("\x1b[H") # Position to top
    printTimeStamp()
    if hasGPS:
        printGPS()
    if hasBMP:
        printBMP()
    if hasHTS:
        printHTS()
    if hasLTR:
        printLTR()
    if hasTSL:
        printTSL()
    if hasSCD:
        printSCD()
    time.sleep(1)
