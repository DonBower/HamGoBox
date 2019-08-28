#!/bin/sh
# install FLAMP (2.2.03) & FLMSG (4.0.6)
#K3HTK 4-5-2018
#Visit http://www.indyham.com

cd /home/pi/HamPi-FLDIGI/

wget -N http://sourceforge.net/projects/fldigi/files/flamp/flamp-2.2.03.tar.gz ||
  { echo 'Can not get flamp file'; exit 1; }

tar -xvzf flamp-2.2.03.tar.gz && cd flamp-2.2.03 ||
  { echo 'Can not extract flamp'; exit 1; }

./configure && sudo make && sudo make install ||
 { echo 'Can not install flamp'; exit 1; }

echo "[Desktop Entry]
Name=Flamp
GenericName=Amateur Radio Digital Modem
Comment=Amateur Radio Sound Card Communications
Exec=flamp
Icon=flamp
Terminal=false
Type=Application
Categories=Network;HamRadio;" > /home/pi/Desktop/flamp.desktop ||
   { echo 'can not setup flamp icon'; exit 1;}

cd /home/pi/HamPi-FLDIGI

wget -N https://sourceforge.net/projects/fldigi/files/flmsg/flmsg-4.0.6.tar.gz ||
 { echo 'Can not get flmsg file'; exit 1; }

tar -xvzf flmsg-4.0.6.tar.gz && cd flmsg-4.0.6 ||
 { echo 'Can not extract flmsg'; exit 1; }

./configure && make && sudo make install ||
 { echo 'Can not install flmsg'; exit 1; }

echo "[Desktop Entry]
Name=Flmsg
GenericName=Amateur Radio Digital Modem
Comment=Amateur Radio Sound Card Communications
Exec=flmsg
Icon=flmsg
Terminal=false
Type=Application
Categories=Network;HamRadio;" > /home/pi/Desktop/flmsg.desktop ||
 { echo 'can not setup flmsg icon'; exit 1;}
