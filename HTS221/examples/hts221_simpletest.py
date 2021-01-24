import os
import time
import board
import busio
import adafruit_hts221

i2c = busio.I2C(board.SCL, board.SDA)
hts = adafruit_hts221.HTS221(i2c)
while True:
    thisHumidity = hts.relative_humidity
    thisTempC = hts.temperature
    thisTempF = 9.0/5.0 * thisTempC + 32

    os.system("echo " + str(thisTempC) + " > ~/console.tempc")
    os.system("echo " + str(thisTempF) + " > ~/console.tempf")
    os.system("echo " + str(thisHumidity) + " > ~/console.humidity")

    print("Relative Humidity: %.2f %% rH" % hts.relative_humidity)
    print("Temperature: %.2f C" % hts.temperature)
    print("")
    time.sleep(1)
