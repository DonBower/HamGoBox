# HamGoBox
Ham Radio Go Box

## Objectives:
The Purpose of this Repository is to document the build of the Ham Radio Go Box, which provides for an encapsulated radio that is already hooked up, and requires only power and an antenna.

## Status:
While the display and python3 code are working very well, there is one piece that needs attention: the humidity trend indicator (↑, →, ↓), needs attention.  it should not be changing from rising, stable, falling more than once an hour, but it changes mid minute.

Additionally, I need better documentation to set up the sensors.
Adafruit has made it very easy to install, and I need to reflect that in this repo.

Lastly, again on the documentation front, the STL files for the 3D printed objects need to be better documented.

## Components:
||||
|:--------:|:---------|:------------------------------------------------------|
| ![alt text][gatorBox] | [Gator Box](https://smile.amazon.com/gp/product/B0002BG4O8/ref=ppx_yo_dt_b_asin_title_o08_s04?ie=UTF8&psc=1) | This 6U Portable Rack keeps all of the equipment in one place, and connected. |
| ![alt text][gatorShelf] | [Shelf](https://smile.amazon.com/gp/product/B01C9KYUG8/ref=ppx_yo_dt_b_asin_title_o08_s01?ie=UTF8&psc=1) | The venting on these shelfs will allow for easy bolting down of equipment. |
| ![alt text][gator1UPanel] | [Blank](https://smile.amazon.com/gp/product/B06Y1VJD6Q/ref=ppx_yo_dt_b_asin_title_o08_s03?ie=UTF8&psc=1) |These aluminum panels will provide a spot to add some meters, connectors and switches|
|![alt text][FT-991]|[FT-991](https://www.yaesu.com/indexVS.cfm?cmd=DisplayProducts&DivisionID=65&ProdCatID=102&encProdID=D24F60F33816ED8BE5568D7E2B5E2131)|While this radio is no longer in production, a newer version (FT-991A) still is.  This Radio has  160M-6M, 2M & 70CM AM/FM/C4FM/SSB/CW.  There is also a digital mode, which lends this radio to doing PSK and other popular modes of communication.|
|![alt text][BATTERY]|[BATTERY](https://www.hamradio.com/detail.cfm?pid=H0-014837)|Lightweight 12 Volt/12 Ah battery based on state-of-the-art Lithium Iron Phosphate electrodes.|
|HF Antenna|[G5RVJR](https://www.hamradio.com/detail.cfm?pid=H0-008917)|40 through 6 meters dipole.|
|VHF/UHF Antenna|[NR-770HB](https://www.hamradio.com/detail.cfm?pid=H0-000063)|Diamond VHF/UHF Mobile Antenna.|
|Antenna Mast|[PNH-22](https://www.hamradio.com/detail.cfm?pid=H0-010315)|Lightweight 22' telescoping fiberglass mast.|
|Antenna Stand|[MFJ-1918](https://www.hamradio.com/detail.cfm?pid=H0-007037)|6 Foot Portable Tripod Antenna Stand.|
|![alt text][wmrPWRGate]|[WMR-Epic PWRgate](https://www.hamradio.com/detail.cfm?pid=H0-015910)|Consolidates power from Battery, Solar and Power Supply sources.  Charges Battery.|
|![alt text][wmr4004U]|[WMR-4004U](https://www.hamradio.com/detail.cfm?pid=H0-009867)|Distributes fused power from Power Gate to various pieces of equipment, including Radio, Raspberry Pi, and Monitor.|
|![alt text][nanoIO]|[Keyer](https://hamprojects.info/mortty/)|This Interface is used to enable True Keyed CW when using fldigi. This is a DIY kit, that requires soldering.|
|![alt text][monitor]|[Monitor](https://smile.amazon.com/gp/product/B07NNXH2SS/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1)|13 inch high res monitor.|
|![alt text][raspberryPI400]|[Computer](https://www.adafruit.com/product/4796)|Yea, that's right Computer. With built in Keyboard.  or peraps the other way around. This computer in a keyboard will run all of the software for the Radio (PSK, Logbook, etc...), it has a USB port, a 40 pin GPIO, and and sd-micro for storage.|
|![alt text][raspberryPIZero]|[Computer](https://www.adafruit.com/product/3708)|This half credit card size computer will run all of the environmental software, it has a USB port, a 40 pin GPIO, and and sd-micro for storage, and it's connected to a boat load of sensors.|
|![alt text][PiTFT]|[Display](https://www.adafruit.com/product/2441)|This Display is configured as the Console for the RaspberryPi. It will display all the Environmental information.|
|![alt text][GPS]|[GPS Sensor](https://www.adafruit.com/product/4415)|Used to determine precise Latitude and Longitude. From this we can derive the Maidenhead Gridsquare.|
|![alt text][SCD-30]|[CO2 Sensor](https://www.adafruit.com/product/4867)|The SCD-30 is an NDIR sensor, which is a 'true' CO2 sensor, that will tell you the CO2 PPM (parts-per-million) composition of ambient air. Unlike the SGP30, this sensor isn't approximating it from VOC gas concentration - it really is measuring the CO2 concentration. Perfect for environmental sensing, scientific experiments, air quality and ventilation studies, and more.|
|![alt text][HTS221]|[Temperature and Humidity Sensor](https://www.adafruit.com/product/4535)|The HTS221 can measure relative humidity from 0%-100% rH with a sensitivity of 0.004% and 3.5% accuracy between 20-80%. It can also measure temperature from -40 to 120 degrees C, with a resolution of 0.016°C with ±0.5 °C accuracy between 15 and +40 °C.|
|![alt text][BMP390]|[Precision Barometric Pressure Sensor](https://www.adafruit.com/product/4816)|The BMP390L is the next-generation of sensors from Bosch, with a low-altitude noise as low as 0.1m and the same fast conversion time. This sensor has a relative accuracy of ±3 Pascals|
|![alt text][LTR390]|[UV Light Sensor](https://www.adafruit.com/product/4831)|The LTR390 has a dedicated  UVA sensor. With both ambient light and UVA sensing with a peak spectral response between 300 and 350nm.|
|![alt text][TSL2591]|[High Dynamic Range Digital Light Sensor](https://www.adafruit.com/product/1980)|The TSL2591 luminosity sensor is an advanced digital light sensor, ideal for use in a wide range of light situations. This Sensor has a dedicated IR light sensor|

<!---
|![alt text][wmrPNP]|[Interface](https://www.hamradio.com/detail.cfm?pid=H0-008403)|This Interface is capable of converting the audio from software sources such as Ham Radio Deluxe (windows onPNH)22https://www.hamradio.com/detail.cfm?pid=H0-010315.  It's also capable of True Keyed CW when used with HRD, but not fldigi.|
--->

---
## Future Wants
* Weather Conditions -rain? wind?
* Power Monitor V/A/W/Batt lifetime
* CAT Monitor
* Ext Speaker

---
## Assembly

---
## Software Installation
* Setup the RaspberryPi

1. OS. I am going to use Rasbian, the default OS for a RaspberryPi. Start by instsalling [NOOBs](http://downloads.raspberrypi.org/NOOBS_latest). The Setup is described in the [Pi](https://github.com/DonBower/HamGoBox/tree/master/Pi)

1. Programs. I am going to use fldig, flrig and wsjt-x. The Setup is described in [fldig](https://github.com/DonBower/HamGoBox/tree/master/fldigi) and [wsjt-x](https://github.com/DonBower/HamGoBox/tree/master/wsjtx)

1. Location. Precise location is always imperative. So we will use [Adafruit's GPS Hat](https://www.adafruit.com/product/2324). The Setup for this device is described in the [GPS Folder](https://github.com/DonBower/HamGoBox/tree/master/GPSHat)

2. Temperature and Humidity. We will be collecting this information with the [DHT22 Sensor](https://www.adafruit.com/product/385). Because Humidity has an effect on the rate of temperature change, it's important to collect the Relative Humidity. Setup will be found in the [DHT22 Folder](https://github.com/DonBower/HamGoBox/tree/master/DHT22)

3. Temperature and Barometric Pressure. Barometric Pressure also has an effect on Temperature, so we will use the [BMP280 Sensor](https://www.adafruit.com/product/2651) to collect this data.  Setup will be found in the [BMP280 Folder](https://github.com/DonBower/HamGoBox/tree/master/BMP280)


[gatorBox]: https://github.com/DonBower/HamGoBox/blob/master/Images/GatorBoxSmall.jpg "Field Day Box"

[gatorShelf]: https://github.com/DonBower/HamGoBox/blob/master/Images/ShelfSmall.jpg "Rack Shelf"

[gator1UPanel]: https://github.com/DonBower/HamGoBox/blob/master/Images/1UPanelSmall.jpg "Blank Panel"

[yaesuFT897D]: https://github.com/DonBower/HamGoBox/blob/master/Images/FT-897DSmall.jpg "Ham Radio"

[FT-991]: https://github.com/DonBower/HamGoBox/blob/master/Images/FT-991.jpg "Ham Radio"

[BATTERY]: https://github.com/DonBower/HamGoBox/blob/master/Images/BLF-1212AS.jpeg "12V12Ah LiFePo Battery"

[wmrPWRGate]: https://github.com/DonBower/HamGoBox/blob/master/Images/WMRPWRgate.jpg "Epic PWRGate"

[wmr4004U]: https://github.com/DonBower/HamGoBox/blob/master/Images/WMR4004U.jpg "RIGrunner 4004U"

[wmrPNP]: https://github.com/DonBower/HamGoBox/blob/master/Images/WMRPnPSmall.jpg "Digital Mode Interface"

[nanoIO]: https://github.com/DonBower/HamGoBox/blob/master/Images/nanoIOSmall.jpg "CW Keyer"

[raspberryPI]: https://github.com/DonBower/HamGoBox/blob/master/Images/RaspberryPiSmall.jpg "Raspberry Pi"

[raspberryPI400]: https://github.com/DonBower/HamGoBox/blob/master/Images/Pi400.jpg "Raspberry Pi 400"

[monitor]: https://github.com/DonBower/HamGoBox/blob/master/Images/monitorSmall.jpg "Monitor"

[raspberryPIZero]: https://github.com/DonBower/HamGoBox/blob/master/Images/RPiZWH.jpg "Raspberry Pi Zero"

[PiTFT]: https://github.com/DonBower/HamGoBox/blob/master/Images/PiTFT.jpg "Raspberry Pi TFT"

[GPS]: https://github.com/DonBower/HamGoBox/blob/master/Images/GPS.jpg "Mini GPS Sensor"

[SCD-30]: https://github.com/DonBower/HamGoBox/blob/master/Images/SCD30.jpg "NDIR CO2 Sensor"

[HTS221]: https://github.com/DonBower/HamGoBox/blob/master/Images/HTS221.jpg "Temperature & Humidity Sensor"

[BMP390]: https://github.com/DonBower/HamGoBox/blob/master/Images/BMP390.jpg "Precision Barometric Pressure and Altimeter Sensor"

[LTR390]: https://github.com/DonBower/HamGoBox/blob/master/Images/LTR390.jpg "UV Light Sensor"

[TSL2591]: https://github.com/DonBower/HamGoBox/blob/master/Images/TSL2591.jpg "High Dynamic Range Digital Light Sensor"
