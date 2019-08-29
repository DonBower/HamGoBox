#!/bin/bash
function get_source_tar() {
  local sourceTAR=$1
  local targetDir=$2
  wget $baseURL/$sourceTar
  tar --directory=$targetDir --extract --gunzip --verbose --file=$sourceTAR
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
programDIR[4]=fldigi
programDIR[3]=flrig
programDIR[2]=hamlib
programDIR[1]=flxmlrc
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

for i in $(echo ${programDIR[@]}); do
  thisProgramDir=${i}
  thisSourceURL=${sourceURL[$thisProgramDir]}
  echo -e "Program Directory....................: ${thisProgramDir}"
  echo -e "Source URL...........................: ${thisSourceURL}"
  get_source_tar ${thisSourceURL} ${thisProgramDir}
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
