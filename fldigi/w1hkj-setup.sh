#!/bin/bash
function get_source_tar(parameter) {
  local baseURL=$1
  local sourceTar=$2
  local targetDir=$3
  wget $baseURL/$sourceTar
  tar --directory=$targetDir --extract --gunzip --verbose --file=$sourceTar
}
devDir=~/Developer
projectDir=$devDir/fldigi
flxmlrpcDir=$projectDir/flxmlrpc
hamlibDir=$projectDir/hamlib
flrigDir=$projectDir/flrig
fldigiDir=$projectDir/fldigi
flxmlrpcVer="0.1.4"
hamlibVer="3.3"
flrigVer="1.3.48"
fldigiVer="4.1.08"

declare -A programDIR
declare -A sourceURL
programDIR[1]=flxmlrc
programDIR[2]=hamlib
programDIR[3]=flrig
programDIR[4]=fldigi
sourceURL[flxmlrc]=http://www.w1hkj.com/files/flxmlrpc/flxmlrpc-${flxmlrpcVer}.tar.gz
sourceURL[hamlib]=https://sourceforge.net/projects/hamlib/files/hamlib/${hamlibVer}/hamlib-${hamlibVer}.tar.gz
sourceURL[flrig]=http://www.w1hkj.com/files/flrig/flrig-${flrigVer}.tar.gz
sourceURL[fldigi]=http://www.w1hkj.com/files/fldigi/fldigi-$fldigiVer.tar.gz

#
# Get Soure Files
#
if [[ ! -d $devDir ]]; then
  mkdir $devDir
fi

if [[ -d $projectDir ]]; then
  rm -rf $projectDir
fi

pushd $projectDir

for i in $(echo ${!programDIR[@]} | sort); do
  echo -e "Program Directory....................: ${programDIR[$i]}"
  echo -e "Source URL...........................: ${sourceURL[$i]}"
  get_source_tar ${sourceURL[$i]} ${programDIR[$i]}
done

exit 0

#
# Enable source repositories
#
sudo --inplace=bak 's/^#deb-src/deb-src/g' /etc/apt/sources.list
sudo apt-get install aptitude
sudo aptitude update
if [[ ! -f /usr/include/X11/Xft/Xft.h ]]; then
  echo "no Xft.h file found --bailing out"
  exit 1
fi
#
# Increase Swap Size
#
swapSizeOld=`grep "CONF_SWAPSIZE=" /etc/dphys-swapfile`
swapSizeNew="CONF_SWAPSIZE=1024"
sudo sed --inplace=bak "s/$swapSizeOld/$swapSizeNew/g" /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
free -m
