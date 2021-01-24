# Tempature and Barametric Pressure sensor
Install with these commands<br>
```
sudo apt-get update
sudo apt-get install git build-essential python-dev python-smbus
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
sudo python setup.py install
```
Then you can run a simple test:
```
cd examples
sudo python simpletest.py
```
Here is what mine looks like:
```
pi@raspberrypi:~/Adafruit_Python_BMP/examples $ sudo python simpletest.py
Temp = 24.50 *C
Pressure = 97255.00 Pa
Altitude = 343.12 m
Sealevel Pressure = 97270.00 Pa
```
