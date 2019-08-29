#!/bin/bash
function get_source_tar() {
  local thisURL=$1
  local thisTAR=$2
  local thisDir=$3
  wget ${thisURL}/${thisTAR}
#  tar --directory=${thisDir} --extract --gunzip --verbose --file=${thisTAR}
  tar --extract --gunzip --file=${thisTAR}
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
declare -A sourceTAR
programDIR[4]=fldigi
programDIR[3]=flrig
programDIR[2]=hamlib
programDIR[1]=flxmlrpc
sourceTAR[flxmlrpc]=flxmlrpc-${flxmlrpcVer}.tar.gz
sourceTAR[hamlib]=hamlib-${hamlibVer}.tar.gz
sourceTAR[flrig]=flrig-${flrigVer}.tar.gz
sourceTAR[fldigi]=fldigi-$fldigiVer.tar.gz
sourceURL[flxmlrpc]=http://www.w1hkj.com/files/flxmlrpc
sourceURL[hamlib]=https://sourceforge.net/projects/hamlib/files/hamlib/${hamlibVer}
sourceURL[flrig]=http://www.w1hkj.com/files/flrig
sourceURL[fldigi]=http://www.w1hkj.com/files/fldigi

#
# Get Soure Files
#
if [[ ! -d $devDir ]]; then
  mkdir $devDir
fi

if [[ -d $projectDir ]]; then
  rm -rf $projectDir/*
else
  mkdir $projectDir
fi

pushd $projectDir

for i in $(echo ${programDIR[@]}); do
  thisProgram=${i}
  thisSourceURL=${sourceURL[$thisProgram]}
  thisSourceTAR=${sourceTAR[$thisProgram]}
  echo -e "Program..............................: ${thisProgram}"
  echo -e "Source URL...........................: ${thisSourceURL}"
  echo -e "Source TAR...........................: ${thisSourceTAR}"
  get_source_tar ${thisSourceURL} ${thisSourceTAR} ${thisProgramDir}
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
