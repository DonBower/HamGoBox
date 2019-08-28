# The Right UART
So Here is my quest to use the Adafruit Ultimate GPS which comes in 2 flavors,   <br>
one is a [breakout](https://www.adafruit.com/products/746), and the other is a [hat](https://www.adafruit.com/products/2324). <br>
The issue with these two products working straight out of the box (with the pi 3) are <br>
1. The UART configured to use the GPIO is disabled <br>
2. The default UART for the GPIO is a mini-UART (i.e. software assisted)<br>
3. The Hardware UART is enabled and configured to use bluetooth.<br>

There is a fantastic write-up on how to get things back on track, which I am ultimately going to follow:  <br>
http://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3  <br>
<br>
First, I am using a [Raspberry Pi 3+](https://www.adafruit.com/products/3055).

<br>
With the Jessie Version of Raspian on my Pi3, the default serial port configuration is:<br>

* `/dev/serial0 -> ttyS0`
  * a.k.a. mini-UART
  * Is configured for GPIO
  * Is disabled
  * uses the service getty to provide console access

* `/dev/serial1 -> ttyAMA0`
  * Is configured for bluetooth
  * Is enabled<br>

These points are demonstrated by displaying the current status of the serial ports:
```
pi@raspberrypi:~/balloon $ ls -l /dev/ser*
lrwxrwxrwx 1 root root 7 Aug 25 03:46 /dev/serial1 -> ttyAMA0
```
We enable the GPIO UART by adding the line `enable_uart=1` to the bottom of <b>/boot/config.txt</b> file and reboot.<br>
<br>
Now we can see both UARTs enabled, but backwards for our purposes:
```
pi@raspberrypi:~/balloon $ ls -l /dev/ser*
lrwxrwxrwx 1 root root 5 Aug 26 02:48 /dev/serial0 -> ttyS0
lrwxrwxrwx 1 root root 7 Aug 26 02:48 /dev/serial1 -> ttyAMA0
```
<br>
Now it's time to stop the console service, which is unnecessary for the balloon project:<br>

```
sudo systemctl stop serial-getty@ttyS0.service
sudo systemctl disable serial-getty@ttyS0.service
```
<br>

Now, let's not reference the console service in future boots.<br>
Remove the `console=serial0,115200` entry from the <b>/boot/cmdline.txt</b> file, and reboot.<br>
<br>
Here is my new <b>/boot/cmdline.txt</b> file:

```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p7 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
```

<br>
Finally we can swap the bluetooth port with the mini-UART by adding the line `dtoverlay=pi3-miniuart-bt` to the bottom of <b>/boot/config.txt</b> and reboot. <br>
<br>

Viola!<br>

```
pi@raspberrypi:~ $ ls -l /dev/ser*
lrwxrwxrwx 1 root root 7 Aug 26 03:24 /dev/serial0 -> ttyAMA0
lrwxrwxrwx 1 root root 5 Aug 26 03:24 /dev/serial1 -> ttyS0
```

Next we need to install the GPS daemon, gpsd. To install gpsd, simply run the following commands from the console:
```
sudo apt-get update
sudo apt-get install gpsd gpsd-clients python-gps
```

This will install the required packages (an internet connection will be required for this step!)
Raspbian Jessie systemd service fix

Now, disable a systemd service that gpsd installs. This service has systemd listen on
a local socket and run gpsd when clients connect to it, however it will also interfere with other gpsd instances that are manually run (like in this guide).

To disable the gpsd systemd service by running the following commands:
```
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
```

After disabling the gpsd systemd service above you're ready to try running gpsd manually. Now run the following command to manually start gpsd and
point it at the GPS breakout on the USB serial adapter port:
```
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
```

... which will point the gps daemon to our GPS device on the onboard serial UART.


Testing it Out
After a few seconds, gpsd should open up the proper socket and if the GPS has locked on to a minimum number of satellites, we should be able to get some data from the GPS module.
To test this, we can use the following command:
```
cgps -s
```

If you have a fix, you'll see something like the following information in the terminal window:
![alt text][logo]

[logo]: https://github.com/DonBower/Eclipse2017/blob/master/GPSHat/cgps%20-s%20output.png "cgps -s output"

<br>

You will need to install a couple more packages to get the rungps.sh script to work:

```
sudo apt install bc
```
<br>
