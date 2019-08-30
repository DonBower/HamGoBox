# TSL2591 python module

This is a simple python library for the Adafruit TSL2591 breakout board based on the [Arduino library](https://github.com/adafruit/Adafruit_TSL2591_Library) from Adafruit. It was developed to work on a Raspberry PI.


# INFO

Enabeling I2C on the Raspberry Pi. You should be fine by following the instruction on [Adafruit](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).

In the last step ('Testing I2C') you should see at least one connected device, your TSL2591 (most likely at 0x29 ).




## Installing ##

To install the python module you first need to install the ibffi-dev package, then compile the driver.


```
sudo apt-get install libffi-dev
sudo python setup.py install
sudo python3 setup.py install
```



## Quickstart ##


```
import tsl2591

tsl = tsl2591.Tsl2591()  # initialize
full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
print lux, full, ir
```




## License ##

Python files in this repository are released under the [MIT license](LICENSE.md).
