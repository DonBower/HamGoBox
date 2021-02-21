# Install the RaspberryPi Imager
Raspberry Pi Imager is the quick and easy way to install Raspberry Pi OS and other operating systems to a microSD card, ready to use with your Raspberry Pi. [Watch their 40-second video](https://www.youtube.com/watch?v=J024soVgEeM) to learn how to install an operating system using Raspberry Pi Imager.

Download and install Raspberry Pi Imager to a computer with an SD card reader. Put the SD card you'll use with your Raspberry Pi into the reader and run Raspberry Pi Imager.

![alt text][Imager]

Install the [RaspberryPi Imager](https://www.raspberrypi.org/software/):

Install on another Raspberry Pi with GUI: run `sudo apt install rpi-imager` in a terminal window

[Download for macOS](https://downloads.raspberrypi.org/imager/imager_1.5.dmg)

[Download for Ubuntu_x86](https://downloads.raspberrypi.org/imager/imager_1.5_amd64.deb)

[Download for Windows](https://downloads.raspberrypi.org/imager/imager_1.5.exe)

[Imager]: https://github.com/DonBower/HamGoBox/blob/master/Images/RPiImager.webp "RaspberryPi Imager"

# Install RasbianOS Lite
Be sure to choose the Lite Version of RasbianOS, because we will not be running a Gui from the RaspberryPi Zero.

Burn the OS image to your MicroSD card using your computer

Re-plug the SD card into your computer (don't use your Pi yet!)

Set up your wifi by copying the file [wpa_supplicant.conf](https://github.com/DonBower/HamGoBox/blob/master/Pi/wpa_supplicant.conf) to the sd card and then edit the file, replacing the <> values with your WiFi name and password.

Create an empty file called ssh on the sd card.
This enables the ssh protocol on the RaspberryPi, which is good, because there is no GUI on this machine.

Plug the SD card into the Pi

If you have an HDMI monitor we recommend connecting it so you can see that the Pi is booting OK

Plug in power to the Pi - you will see the green LED flicker a little. The Pi will reboot while it sets up so wait a good 10 minutes

If you are running Windows on your computer, install Bonjour support so you can use .local names, you'll need to reboot Windows after installation

You can now ssh into raspberrypi.local
`ssh pi@raspberrypi.local`

# Set Hostname
```
sudo echo hampi > /etc/Hostname
sudo shutdown -r now
```

The Pi will reboot so log back in with `ssh pi@hampi.local`

# SSH Interface

Next order of business is get a ssh key. (Take all defaults)

```
ssh-keygen
```
Now, log out of the session with `exit` and copy the public key on your linux based machine to the RaspberryPi, so you don't have to use a password each time you log in.

```
ssh-copy-id -i ~/.ssh/mykey pi@hampi.local
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

# I2C Interface
To setup the [I2C (Inter-Integrated Circuit)](https://en.wikipedia.org/wiki/I%C2%B2C)
Interface, execute the following:

```
sudo apt-get --assume-yes install python-smbus
sudo apt-get --assume-yes install i2c-tools
```
Then use `sudo raspi-config` to enable the Interface.

View the connected devices:
```
sudo i2cdetect -y 1
```

# Setup Tools

```
sudo pip3 install --upgrade setuptools\
```

# From Adafruit


Installing CircuitPython Libraries on Raspberry Pi
 Like
CircuitPython libraries and adafruit-blinka will work on any Raspberry Pi board! That means the original 1, the Pi 2, Pi 3, Pi 4, Pi Zero, or even the compute module.
Prerequisite Pi Setup!
In this page we'll assume you've already gotten your Raspberry Pi up and running and can log into the command line

Here's the quick-start for people with some experience:

Download the latest Raspberry Pi OS or Raspberry Pi OS Lite to your computer
Burn the OS image to your MicroSD card using your computer
Re-plug the SD card into your computer (don't use your Pi yet!) and set up your wifi connection by editing supplicant.conf
Activate SSH support
Plug the SD card into the Pi
If you have an HDMI monitor we recommend connecting it so you can see that the Pi is booting OK
Plug in power to the Pi - you will see the green LED flicker a little. The Pi will reboot while it sets up so wait a good 10 minutes
If you are running Windows on your computer, install Bonjour support so you can use .local names, you'll need to reboot Windows after installation
You can then ssh into raspberrypi.local
The Pi Foundation has tons of guides as well

We really really recommend the lastest Raspberry Pi OS only. If you have an older Raspberry Pi OS install, run "sudo apt-get --assume-yes update" and "sudo apt-get --assume-yes upgrade" to get the latest OS!
Update Your Pi and Python
Run the standard updates:

```
sudo apt-get --assume-yes update
sudo apt-get --assume-yes upgrade
sudo apt-get --assume-yes install python3-pip
sudo pip3 install --upgrade setuptools
cd ~
sudo pip3 install --upgrade adafruit-python-shell click==7.0
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
```

ls /dev/i2c* /dev/spi*

You should see the response

/dev/i2c-1 /dev/spidev0.0 /dev/spidev0.1
