#!/usr/bin/python3
import os
from os import path
import sys
import time
from datetime import datetime
from datetime import timedelta
import requests
import xml.etree.ElementTree as ET
import json
import board
import busio
import adafruit_gps
import adafruit_bmp3xx
import adafruit_hts221
import adafruit_ltr390
import adafruit_tsl2591
import adafruit_scd30

xmlFile = '/tmp/solarrss.xml'
now = datetime.now()
freshDate = now + timedelta(hours = 12)

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
# Convert Decimal Degrees to degrees, minutes, and seconds
#
def getSexagesimal(decDegrees, latlon):
    thisDegree = int(abs(decDegrees))
    decMinSec  = abs(decDegrees) - thisDegree
    thisMin    = int(decMinSec * 60)
    decSec     = decMinSec - (thisMin / 60)
    thisSec    = round((decSec * 3600), 3)
    thisSexagesimal  = str(thisDegree) + '° '
    thisSexagesimal += str(thisMin).zfill(2) + '\' '
    thisSexagesimal += str(thisSec).zfill(2) + '" '
    if decDegrees >= 0:
        thisSexagesimal += str(latlon[0])
    else:
        thisSexagesimal += str(latlon[1])
    return thisSexagesimal

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

#    thisLat = 34
#    thisLon = -117

    print(f'Maidenhead.........: {getMaidenHead(thisLat, thisLon):8s}                   '[:40], end='')
    print(f'Lat/Lon ({thisSatCount:02d}).......: {thisLat:07.4f} / {thisLon:08.4f}                   '[:40], end='')
#    print(f'Lat/Lon ({thisSatCount:02d}).......: {getSexagesimal(thisLat,["N","S"]):16s} / {getSexagesimal(thisLon,["N","S"]):17s}                   '[:40], end='')
    print(f'Altitude...........: {thisAltM:5,.1f}M / {thisAltF:3,.0f}F                   '[:40], end='')

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
#    °c/°f
#    ℃/℉ - These do not print.
    print(f'Temperature........: {thisTempC:4.1f}°C /{thisTempF:5.1f}°F                   '[:40])
    print(f'Relative Humidity..: {thisHumidity:4.1f}% rH                   '[:40])

def printLTR():
    thisUV           = ltr.uvs
#    thisUVi          = int(round((thisUV / 95), 0))
    thisUVi          = ltr.uvi
#    thisAmbient      = ltr.light
    thisAmbient      = ltr.lux
    print(f'UVa EMF / UVI......: {thisUV:1,d}µW/cm^2 / {thisUV:1,d}UVi                   '[:40])
    print(f'Ambient Light......: {thisAmbient:1,.1f}                   '[:40])

def printTSL():
    thisIR           = tsl.infrared
    thisVis          = tsl.visible
    thisLux          = tsl.lux
    thisFullSpectrum = tsl.full_spectrum
    print(f'Visable Light......: {thisVis:4,d}                   '[:40])
    print(f'Infrared Light.....: {thisIR:1,d}                   '[:40])

def printLight():
    if hasTSL:
        thisIR       = tsl.infrared
        thisVis      = tsl.visible/1000
    else:
        thisIR       = 0
        thisVis      = 0
    if hasLTR:
        thisUV       = ltr.uvs
        thisUVi      = ltr.uvi
        if thisVis == 0:
            thisVis  = ltr.lux * 1000
    if hasTSL and hasLTR:
        print(f'IR/Visable/UVI.....: {thisIR:1,d} / {thisVis:1,.0f} / {thisUV:1,d}                   '[:40])
    elif hasLTR:
        print(f'Visable/UVI........: {thisVis:1,.0f} / {thisUV:1,d}                   '[:40])
    elif hasTSL:
        print(f'IR/Visable.........: {thisIR:1,d} / {thisVis:1,.0f}                   '[:40])


def printSCD():
    global thisCO2
    if scd.data_available:
        thisCO2      = scd.CO2
    if thisCO2 > 5000:
        thisCO2Lvl   = '(!Danger!)'
    elif thisCO2 > 2000:
        thisCO2Lvl   = '..(*High*)'
    elif thisCO2 > 1000:
        thisCO2Lvl   = '(Elevated)'
    elif thisCO2 > 400:
        thisCO2Lvl   = '..(Normal)'
    else:
        thisCO2Lvl   = '.....(Low)'
    print(f'CO2......{thisCO2Lvl:10s}: {thisCO2:3,.1f}ppm                   '[:40], end='')

def bandIndex(thisBand):
    switcher={
        '80m-40m':0,
        '30m-20m':1,
        '17m-15m':2,
        '12m-10m':3
        }
    return switcher.get(thisBand,"Invalid Band")

def timeIndex(thisTime):
    switcher={
            'day':0,
            'night':1
         }
    return switcher.get(thisTime,"Invalid Time")

def getRSS(xmlFile):
    # url of rss feed
    url = 'http://www.hamqsl.com/solarrss.php'
    # creating HTTP response object from given url
    resp = requests.get(url)
    # saving the xml file
    with open(xmlFile, 'wb') as f:
        f.write(resp.content)

def parseRSS(xmlFile):
    global thisMUF, theseConditions, freshDate
    # create element tree object
    tree = ET.parse(xmlFile)
    # get root element
    root = tree.getroot()

    fileDate=root.findall('./channel/item/solar/solardata/updated')[0].text
    rssDate=datetime.strptime(fileDate," %d %b %Y %H%M %Z")
    freshDate = rssDate + timedelta(hours = 12)

    solarData = root.findall('./channel/item/solar/solardata')
    thisMUF=root.findall('./channel/item/solar/solardata/muf')[0].text
    # create empty list for news items
    theseConditions = [['' for x in range(4)] for y in range(2)]
    # iterate news items
    for band in root.findall('./channel/item/solar/solardata/calculatedconditions/band'):
        thisBand=band.attrib['name']
        thisTime=band.attrib['time']
        thisCondition=band.text
        theseConditions[timeIndex(thisTime)][bandIndex(thisBand)] = thisCondition

def printSolar():
    print(f'------------------------------------------------                    '[:40])
    print(f'MUF={thisMUF:5s}|80m-40m|30m-20m|17m-15m|12m-10m                    '[:40])
    print(f'Day      |{theseConditions[0][0]:^7s}|{theseConditions[0][1]:^7s}|{theseConditions[0][2]:^7s}|{theseConditions[0][3]:^7s}                    '[:40])
    print(f'Night    |{theseConditions[1][0]:^7s}|{theseConditions[1][1]:^7s}|{theseConditions[1][2]:^7s}|{theseConditions[1][3]:^7s}                    '[:40], end='')

if not path.exists(xmlFile):
    getRSS(xmlFile)

parseRSS(xmlFile)

clearScreen()
while True:
#    sys.stdout.write("\x1b[2J\x1b[H") # Position to top
    sys.stdout.write("\x1b[H") # Position to top
    now = datetime.now()
    printTimeStamp()
    if not divmod(int(datetime.now().strftime("%S")),6)[1]:
        if hasGPS:
            printGPS()
        if hasHTS:
            printHTS()
        if hasBMP:
            printBMP()
        if hasSCD:
            printSCD()
        if hasLTR or hasTSL:
            printLight()
#        if hasLTR:
#            printLTR()
#        if hasTSL:
#            printTSL()
        if now > freshDate:
            getRSS(xmlFile)
            parseRSS(xmlFile)
        printSolar()
    time.sleep(1)
