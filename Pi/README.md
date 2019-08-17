# Connect to network

First order of business, was to connect to my WiFi, which had to be done via the KVM Interface.  Click on the Network Interface Icon, which is two Xs and just to the left of the speaker icon, to show the available WiFi Routers.
<br>

![alt text][WiFi]

[WiFi]: https://github.com/DonBower/Eclipse2017/blob/master/Pi/SelectWiFi.png "Select WiFi"

<br>

Enter the Password...
<br>

![alt text][Password]

[Password]: https://github.com/DonBower/Eclipse2017/blob/master/Pi/EnterWiFiPassword.png "Enter WiFi Password"

<br>

After a few moments, your RaspberryPi should be connected to the network.  Hover the mouse over the WiFi Icon to show the status and address:

<br>

![alt text][Connected]

[Connected]: https://github.com/DonBower/Eclipse2017/blob/master/Pi/WiFiConnected.png "Your WiFi is connected"

<br>


# Firmware/OS Updates

Next we update/upgrade the OS to the latest version, as well as the RaspberryPi Firmware.  <br />

```
sudo apt-get update
sudo rpi-update
```

At this point, your system may have actually performed a firmware update.  And a brave man may continue on and reboot later.  I am not that brave. `sudo shutdown -r now` if you are so inclined.


```
sudo apt-get upgrade
sudo apt-get dist-upgrade
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

[Main]: https://github.com/DonBower/Eclipse2017/blob/master/Pi/Interfacing%20Options.png "raspi-config Main Screen"

<br>

![alt text][P2SSH]

[P2SSH]: https://github.com/DonBower/Eclipse2017/blob/master/Pi/P2%20Enable%20SSH.png "raspi-config P2 Enable SSH"

<br>

![alt text][SSH]

[SSH]: https://github.com/DonBower/Eclipse2017/blob/master/Pi/Enable%20SSH.png "raspi-config Enable SSH"

<br>

Reboot with `sudo shutdown -r now`


# Git/GitHub

Then it's time to get git, and configure the git Global Variables <br />

```
sudo apt-get install git
git config --global user.name "Don Bower"
git config --global user.email "Don.Bower@outlook.com"
```

Next Create a *Developer* directory, and clone this repository from there.  The *Developer* directory is standard practice for modern developers. Some use lowercase for the name, but since on the RaspberryPi, and my Mac, all the other preloaded directories are capitalized, (i.e. Documents, Pictures, etc...) I'll follow form. <br />

```
mkdir ~/Developer
cd ~/Developer
git clone git@github.com:DonBower/Eclipse2017.git
```

If you need updates from github, use git pull:

```
cd ~/Developer/Eclipse2017
git pull origin master
```

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

[DFH]: https://github.com/DonBower/Eclipse2017/blob/master/Pi/DF%20-h%20output.png "df -h output example"

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
  sudo mkfs.ext4 -L Eclipse2017 /dev/sda1
  ```

The follow steps will allow the USB drive to be persistently mounted.

```
sudo mkdir /mnt/usbstick
sudo chmod 777 /mnt
sudo chmod 777 /mnt/usbstick
sudo tee -a /etc/fstab <<EOF
LABEL=Eclipse2017     /mnt/usbstick   ext4    defaults          0       1
EOF
sudo mount -a
```

You should now be able to `df -h` and see the /dev/sda1 mounted on /mnt/usbstick.

# I2C Interface
To setup the [I2C (Inter-Integrated Circuit)](https://en.wikipedia.org/wiki/I%C2%B2C)
Interface, execute the following:

```
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
```
Then use `sudo raspi-config` to enable the Interface.

View the connected devices:
```
sudo i2cdetect -y 1
```

# Autostart
To start the four programs automatically on boot (useful for use when you have no access to the pi in the field), edit the crontab (`sudo crontab -e -u pi`) and add the following line:

```
@reboot /home/pi/Developer/Eclipse2017/startup.sh
```
