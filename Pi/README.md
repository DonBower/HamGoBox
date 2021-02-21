# Install the RaspberryPi Imager
Raspberry Pi Imager is the quick and easy way to install Raspberry Pi OS and other operating systems to a microSD card, ready to use with your Raspberry Pi. [Watch their 40-second video](https://www.youtube.com/watch?v=J024soVgEeM) to learn how to install an operating system using Raspberry Pi Imager.

Download and install Raspberry Pi Imager to a computer with an SD card reader. Put the SD card you'll use with your Raspberry Pi into the reader and run Raspberry Pi Imager.
Install on another Raspberry Pi with GUI: run `sudo apt install rpi-imager` in a terminal window

Install the [RaspberryPi Imager](https://www.raspberrypi.org/software/):
![alt text][Imager](https://www.raspberrypi.org/software/)

[Download for macOS](https://downloads.raspberrypi.org/imager/imager_1.5.dmg)

[Download for Ubuntu_x86](https://downloads.raspberrypi.org/imager/imager_1.5_amd64.deb)

[Download for Windows](https://downloads.raspberrypi.org/imager/imager_1.5.exe)

[Imager]: https://github.com/DonBower/HamGoBox/blob/master/Images/RPiImager.webp "RaspberryPi Imager"

# Install RasbianOS Lite
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



# Connect to network

First order of business, was to connect to my WiFi, which had to be done via the KVM Interface.  Click on the Network Interface Icon, which is two Xs and just to the left of the speaker icon, to show the available WiFi Routers.
<br>

![alt text][WiFi]

[WiFi]: https://github.com/DonBower/HamGoBox/blob/master/Pi/SelectWiFi.png "Select WiFi"

<br>

Enter the Password...
<br>

![alt text][Password]

[Password]: https://github.com/DonBower/HamGoBox/blob/master/Pi/EnterWiFiPassword.png "Enter WiFi Password"

<br>

After a few moments, your RaspberryPi should be connected to the network.  Hover the mouse over the WiFi Icon to show the status and address:

<br>

![alt text][Connected]

[Connected]: https://github.com/DonBower/HamGoBox/blob/master/Pi/WiFiConnected.png "Your WiFi is connected"

<br>


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

# SSH Interface

Next order of business is get a ssh key. (Take all defaults)

```
ssh-keygen
```

Copy the public SSH key to GitHub per the instructions documented in https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/<br>

Now is a perfect oppertunity to enable SSH, so that you can access your Pi via terminal from other devices.

`sudo raspi-config`
Interfacing Options > P2 Enable SSH > Enable SSH.
<br>

![alt text][Main]

[Main]: https://github.com/DonBower/HamGoBox/blob/master/Pi/Interfacing%20Options.png "raspi-config Main Screen"

<br>

![alt text][P2SSH]

[P2SSH]: https://github.com/DonBower/HamGoBox/blob/master/Pi/P2%20Enable%20SSH.png "raspi-config P2 Enable SSH"

<br>

![alt text][SSH]

[SSH]: https://github.com/DonBower/HamGoBox/blob/master/Pi/Enable%20SSH.png "raspi-config Enable SSH"

<br>

Reboot with `sudo shutdown -r now`


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
git pull origin master
```

***

# External Storage (USB Stick)

In addition to the RaspberryPi, we need a storage device for all the data we will collect.
I'm not really sure at this time what size we need, so I'll go big, and use the [Samsung 32GB USB 3.0 Flash Drive Fit](https://www.amazon.com/Samsung-Flash-Drive-MUF-32BB-AM/dp/B013CCTOC2) from amazon.
First, find any unintentional mounts from plugging in the flash drive. (Note: the procedures below assume the device is /dev/sda, and therefore the partition is /dev/sda1.  Should the next command display a different device, you must adapt as required.)

  ```
  df -h
  ```

look for devices mounted to /dev/sda*, and unmount them.  For example if you see a directory mounted on /dev/sda1, as I did with my Samsung-Flash-Drive-MUF-32BB, then run this command to unmount it.

<br>

![alt text][DFH]

[DFH]: https://github.com/DonBower/HamGoBox/blob/master/Pi/DF%20-h%20output.png "df -h output example"

<br>


  ```
  sudo umount /dev/sda1
  ```

Next, *and this is destructive*, remove any partitions, and create a new, fresh one.

  ```
  sudo fdisk /dev/sda
  p # This will print all the partitions
  d # This will delete the last partition. Repeat as required to delete all partitions
  n # This will create a new partition.  Take all the defaults.
  w # Rewrite the new partition table.
  ```

Now, format the new partition for ext4 file system.

  ```
  sudo mkfs.ext4 -L HamGoBox /dev/sda1
  ```

The follow steps will allow the USB drive to be persistently mounted.

```
sudo mkdir /mnt/usbstick
sudo chmod 777 /mnt
sudo chmod 777 /mnt/usbstick
sudo tee -a /etc/fstab <<EOF
LABEL=HamGoBox     /mnt/usbstick   ext4    defaults          0       1
EOF
sudo mount -a
```

You should now be able to `df -h` and see the /dev/sda1 mounted on /mnt/usbstick.

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


# From Adafruit
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
