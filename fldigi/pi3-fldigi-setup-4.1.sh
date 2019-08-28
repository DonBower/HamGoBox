#!/bin/bash
# install HamPi-FLDIGI(4.1)
#K3HTK 3-1-2019
#Hamlib Updated to 3.3 on 2-17-2019
#Removed libportaudio-dev and Replaced with portaudio19-dev
#Visit http://www.indyham.com
#Email: mailto:k3htk@arrl.net

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install git cmake build-essential libusb-1.0-0.dev libltdl-dev libusb-1.0-0 libhamlib-utils libsamplerate0 libsamplerate0-dev libsigx-2.0-dev libsigc++-1.2-dev libpopt-dev tcl8.5-dev libspeex-dev libasound2-dev alsa-utils libgcrypt11-dev libpopt-dev libfltk1.3-dev libpng++-dev portaudio19-dev libpulse-dev libportaudiocpp0 libsndfile1-dev ||
	{ echo 'Retrieving dependencies failed'; exit 1;}

#Comment - If the HamPi-FLDIGI directory does exist, skip. If not, create it!
mkdir -p /home/pi/HamPi-FLDIGI && cd HamPi-FLDIGI ||
	{ echo 'Can not create or find HamPi-FLDIGI dir'; exit 1; }

#Comment - Remove old directories used for installing previous version(s) of fldigi
sudo rm -rf fldigi-* ||
        { echo 'ERROR - Failed to proceed after fldigi DIR removal'; exit 1; }

#Comment - Remove old directories used for installing previous version(s) of hamlib
sudo rm -rf hamlib-* ||
        { echo 'ERROR - Failed to proceed after hamlib DIR removal'; exit 1; }

#Comment - Download Hamlib 3.3 Version from SourceForge
wget -N --trust-server-names https://sourceforge.net/projects/hamlib/files/hamlib/3.3/hamlib-3.3.tar.gz ||
	{ echo 'Cannot download HamLib file'; exit 1; }

#Comment - Extract hamlib tarball
tar -xvzf hamlib*

#Comment - Allow extract to finish before CD to Dir
sleep 5

#Comment - Change directory after hamlib file extracted
cd $(find $hamlib* | head -1)

#Comment - Run command to build and install hamlib
./configure && make && sudo make install ||
	{ echo 'Can not install HamLib'; exit 1; }

sudo ldconfig

sudo apt-get -y install portaudio19-dev ||
	{ echo 'Cannot install Portaudio dependency'; exit 1;}

#Change directory up level from HamLib Process
cd .. ||

#Comment - New way of checking for additional releases

set -eu

urls=( https://sourceforge.net/projects/fldigi/files/fldigi/fldigi-4.1.{20..00}.tar.gz )
for url in "${urls[@]}"; do
  set +e
  http_status=$( wget --server-response -c "$url" 2>&1 )
  exit_status=$?
  http_status=$( awk '/HTTP\//{ print $2 }' <<<"$http_status" | tail -n 1 )

  if (( http_status >= 400 )); then
    # Considering only HTTP Status errors
    case "$http_status" in
      # Define your actions for each 4XX Status Code below
      410) : Gone
        ;;
      416) : Requested Range Not Satisfiable
        ;;
      403) : Forbidden
        ;&
      404) : Not Found
    esac
  elif (( http_status >= 300 )); then
     # We're unlikely to reach here in case of 1XX, 3XX in $http_status
     # but ..
        echo 'made it to 300 ERR'
  elif (( http_status >= 200 )); then
     # 2XX in $http_status considered successful
        echo 'made it to 200 SUCCESS'
     break 
  fi
  echo "$url -> http_status: $http_status" >&2
done

tar -kxzf fldigi-4.* ||
  { echo 'Can not extract fldigi'; exit 1; }

# Comment change directory to Fldigi Extract
cd $(find $fldigi* | head -1) 

./configure --with-portaudio && make && sudo make install ||
  { echo 'Can not install fldigi'; exit 1; }

cd .. && wget -N http://www.elazary.com/images/mediaFiles/ham/hampi/setGPIO ||
  { echo 'Can not get setGPIO'; exit 1; }

if ! grep -q setGPIO ~/.bashrc  ; then 
  echo "sudo sh /home/pi/HamPi-FLDIGI/setGPIO" >> ~/.bashrc
fi

if ! grep -q snd-mixer-oss /etc/modules  ; then 
  sudo sh -c "echo snd-mixer-oss >> /etc/modules"
fi

if ! grep -q snd-pcm-oss /etc/modules  ; then 
  sudo sh -c "echo snd-pcm-oss >> /etc/modules"
fi

echo "[Desktop Entry]
Name=Fldigi
GenericName=Amateur Radio Digital Modem
Comment=Amateur Radio Sound Card Communications
Exec=fldigi
Icon=fldigi
Terminal=false
Type=Application
Categories=Network;HamRadio;" > /home/pi/Desktop/fldigi.desktop ||
   { echo 'Cannot setup fldigi icon'; exit 1;}

echo 'Setup Complete! Enjoy... de K3HTK'
