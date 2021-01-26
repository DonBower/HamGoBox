# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_bmp3xx
import os

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# SPI setup
# from digitalio import DigitalInOut, Direction
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# cs = DigitalInOut(board.D5)
# bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)

bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

while True:
    hPa = bmp.pressure
    os.system("echo " + str(hPa) + " > ~/console.hPa")
    tempc = bmp.temperature
    tempf = 9.0/5.0 * tempc + 32
    os.system("echo " + str(tempc) + " > ~/console.tempc")
    os.system("echo " + str(tempf) + " > ~/console.tempf")

    print(
        "Pressure: {:6.4f}  Temperature: {:5.2f}".format(hPa, tempc)
    )
    time.sleep(1)
