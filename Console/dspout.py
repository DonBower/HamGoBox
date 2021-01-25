#!//usr/bin/python3
import os
import sys
import time
from datetime import datetime
import board
import busio
import adafruit_gps
import adafruit_bmp3xx
import adafruit_hts221

#last_print = time.monotonic()

i2c = busio.I2C(board.SCL, board.SDA)
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

print(hasGPS)

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

print(hasBMP)

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

print(hasBMP)

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
    print("Timestamp..........: " + timeStampNow + "\n")
#
# Print GPS Latitude, Longitude and Maidenhead
#
def getMaidenHead(latitude, longitude):
    maxMaiden  = 4
    A          = ord('A')
    a          = divmod((longitude + 180),20)
    b          = divmod((latitude + 90),10)
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
    thisAltitude = gps.altitude_m
    thisSatCount = gps.satellites
    print(f'Maidenhead.........: {getMaidenHead(thisLat, thisLon):8s}')
    print(f'Lat/Lon ({thisSatCount:02d}).......: {thisLat:07.4f} / {thisLon:08.4f}')
    print(f'Altitude...........: {thisAltitude:06.1f}m')

def printBMP():
    thisPressure = bmp.pressure
    print(f'Barometric Pressure: {thisPressure:05.2f} hPa')

def printHTS():
    thisHumidity = hts.relative_humidity
    thisTempC    = hts.temperature
    thisTempF    = ((9.0 / 5.0) * thisTempC + 32)
    print(f'Temp...............: {thisTempC:4.1f}°c /{thisTempF:5.1f}°f')
    print(f'Relative Humidity..: {thisHumidity:4.1f} % rH')

clearScreen()
while True:
    sys.stdout.write("\x1b[2J\x1b[H") # Position to top
    printTimeStamp()
    if hasGPS:
        printGPS()
    if hasBMP:
        printBMP()
    if hasHTS:
        printHTS()
    time.sleep(1)
