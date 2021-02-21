# Install the RaspberryPi Imager
Raspberry Pi Imager is the quick and easy way to install Raspberry Pi OS and other operating systems to a microSD card, ready to use with your Raspberry Pi. [Watch their 40-second video](https://www.youtube.com/watch?v=J024soVgEeM) to learn how to install an operating system using Raspberry Pi Imager.

Download and install Raspberry Pi Imager to a computer with an SD card reader. Put the SD card you'll use with your Raspberry Pi into the reader and run Raspberry Pi Imager.

![alt text][Imager]

Install the [RaspberryPi Imager](https://www.raspberrypi.org/software/):

* Install on another Raspberry Pi with GUI: run `sudo apt install rpi-imager` in a terminal window

* [Download for macOS](https://downloads.raspberrypi.org/imager/imager_1.5.dmg)

* [Download for Ubuntu_x86](https://downloads.raspberrypi.org/imager/imager_1.5_amd64.deb)

* [Download for Windows](https://downloads.raspberrypi.org/imager/imager_1.5.exe)

[Imager]: https://github.com/DonBower/HamGoBox/blob/master/Images/RPiImager.webp "RaspberryPi Imager"

# Install RasbianOS Lite
Be sure to choose the Lite Version of RasbianOS, because we will not be running a Gui from the RaspberryPi Zero.

Burn the OS image to your MicroSD card using your computer

Re-plug the SD card into your computer (don't use your Pi yet!)

Set up your wifi by copying the file [wpa_supplicant.conf](https://github.com/DonBower/HamGoBox/blob/master/Pi/wpa_supplicant.conf) to the sd card and then edit the file, replacing the <> values with your WiFi name and password.

Create an empty file called ssh on the sd card.
```
touch /Volumes/boot/ssh
```
This enables the ssh protocol on the RaspberryPi, which is good, because there is no GUI on this machine.

Eject the SD Card from your PC, and plug it into the Pi

If you have an HDMI monitor we recommend connecting it so you can see that the Pi is booting OK

Plug in power to the Pi - you will see the green LED flicker a little. The Pi will reboot while it sets up so wait a good 10 minutes

If you are running Windows on your computer, install Bonjour support so you can use .local names, you'll need to reboot Windows after installation

You can now ssh into raspberrypi.local
`ssh pi@raspberrypi.local`

# Set Hostname
```
sudo sed -i 's/raspberrypi/goboxpi/g' /etc/hosts
sudo sed -i 's/raspberrypi/goboxpi/g' /etc/hostname
sudo shutdown -r now
```

The Pi will reboot so log back in with `ssh pi@goboxpi.local`

# SSH Interface

Next order of business is get a ssh key. (Take all defaults)

```
ssh-keygen
```
Now, log out of the session with `exit` and copy the public key on your linux based machine to the RaspberryPi, so you don't have to use a password each time you log in.

```
ssh-copy-id -i ~/.ssh/id_rsa.pub pi@goboxpi.local
```

Copy the public SSH key to GitHub per the instructions documented in https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/<br>

# Firmware/OS Updates

Next we update/upgrade the OS to the latest version, as well as the RaspberryPi Firmware.  <br />

```
sudo apt-get --assume-yes update
sudo rpi-update
```

At this point, your system may have actually performed a firmware update.  And a brave man may continue on and reboot later.  I am not that brave. `sudo shutdown -r now` if you are so inclined.


```
sudo apt-get --assume-yes upgrade
sudo apt-get --assume-yes dist-upgrade
sudo shutdown -r now
```

# Set Timezone

Set the Timezone

```
sudo timedatectl set-timezone America/Los_Angeles
```

# Git/GitHub

Then it's time to get git, and configure the git Global Variables <br />
(note: use your own name and email...)

```
sudo apt-get --assume-yes install git
git config --global user.name "Don Bower"
git config --global user.email "Don.Bower@outlook.com"
```

Next Create a *Developer* directory, and clone this repository from there.  The *Developer* directory is standard practice for modern developers. Some use lowercase for the name, but since on the RaspberryPi, and my Mac, all the other preloaded directories are capitalized, (i.e. Documents, Pictures, etc...) I'll follow form. <br />

```
mkdir ~/Developer
cd ~/Developer
git clone git@github.com:DonBower/HamGoBox.git
```

If you need updates from github, use git pull:

```
cd ~/Developer/HamGoBox
git pull
```

# Setup Tools

```
sudo pip3 install --upgrade setuptools
```
If above doesn't work, install pip3 and try again.

```
sudo apt-get install python3-pip
```
Adafruit put together a script to easily make sure your Pi is correctly configured and install Blinka. It requires just a few commands to run. Most of it is installing the dependencies.
```
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
```
select Y for any prompts.
after the RaspberryPi has rebooted, run this Test to confirm all the interfaces were installed and enabled

The [I&#x00B2;C (Inter-Integrated Circuit)](https://en.wikipedia.org/wiki/I%C2%B2C) and spi interfaces should now be installed and enabled.


You can run the following command to verify:
```
python3 Developer/HamGoBox/Pi/blinkatest.py
```

You can run the following command to verify:
```
ls /dev/i2c* /dev/spi*
```
You should see the response
```
/dev/i2c-1 /dev/spidev0.0 /dev/spidev0.1
```

# Python SMBUS and I&#x00B2;C Interface tools
To view the [I&#x00B2;C (Inter-Integrated Circuit)](https://en.wikipedia.org/wiki/I%C2%B2C)
devices that are connected, execute the following:
```
sudo i2cdetect -y 1
```
Your output will look similar to the following:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: 10 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- 29 -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- 53 -- -- -- -- -- -- -- -- -- -- -- 5f
60: -- 61 -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- 77                         
```
all of the non "--" entries represent a device detected.


# Install CircuitPython Libraries for the sensors:

```
sudo pip3 install adafruit-circuitpython-gps \
 adafruit-circuitpython-bmp3xx \
 adafruit-circuitpython-hts221 \
 adafruit-circuitpython-tsl2591 \
 adafruit-circuitpython-ltr390 \
 adafruit-circuitpython-scd30
```

Test Which sensors are installed:
```
python3 ~/Developer/HamGoBox/Pi/sensortest.py
```

# Install TFT Display as the console.

```
cd ~
sudo pip3 install --upgrade adafruit-python-shell click==7.0
sudo apt-get install -y git
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts
sudo python3 adafruit-pitft.py --display=35r --rotation=90 --install-type=console
```





# Install Blinka from Adafruit
```
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
```
