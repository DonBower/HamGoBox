# Install 3.5" PiTFT
cd ~
sudo pip3 install --upgrade adafruit-python-shell click==7.0
sudo apt-get install -y git
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts
sudo python3 adafruit-pitft.py --display=35r --rotation=90 --install-type=console --reboot=yes
Rebooting
If/When it asks you to reboot, then choose yes because the setting won't take full effect until you do so.

# Autostart
To start the four programs automatically on boot (useful for use when you have no access to the pi in the field), edit the crontab (`sudo crontab -e -u root`) and add the following line:

```
@reboot /home/pi/Developer/HamGoBox/Console/dspout.sh 1> /home/pi/dspout.sh.errlog.txt 2>&1
```

# Display
Here is the display:
note: the GPS values are captured before satellite lock.

![alt text][hampiwx]

[hampiwx]: https://github.com/DonBower/HamGoBox/blob/master/Images/IMG_0802.jpeg "HamPiWX Console"

from a keyboard, use the command dspkill.sh to kill the auto-restart and python process