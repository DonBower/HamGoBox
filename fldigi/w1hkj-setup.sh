#!/bin/bash
function get_source_tar() {
  local thisURL=$1
  local thisTAR=$2
  local thisDir=$3
  wget ${thisURL}/${thisTAR}
  tar --extract --gunzip --file=${thisTAR}
}

function compile_source() {
  local thisDir=$1
  pushd $thisDir
  ./configure
  make
  sudo make install
  popd
}

devDir=~/Developer
projectDir=$devDir/fldigi

flxmlrpcVer="0.1.4"
hamlibVer="3.3"
flrigVer="1.3.48"
fldigiVer="4.1.08"

declare -A programName
declare -A sourceURL
declare -A sourceTAR
declare -A sourceDIR
programName[4]=fldigi
programName[3]=flrig
programName[2]=hamlib
programName[1]=flxmlrpc
sourceURL[flxmlrpc]=http://www.w1hkj.com/files/flxmlrpc
sourceURL[hamlib]=https://sourceforge.net/projects/hamlib/files/hamlib/${hamlibVer}
sourceURL[flrig]=http://www.w1hkj.com/files/flrig
sourceURL[fldigi]=http://www.w1hkj.com/files/fldigi

sourceTAR[flxmlrpc]=flxmlrpc-${flxmlrpcVer}.tar.gz
sourceTAR[hamlib]=hamlib-${hamlibVer}.tar.gz
sourceTAR[flrig]=flrig-${flrigVer}.tar.gz
sourceTAR[fldigi]=fldigi-$fldigiVer.tar.gz

sourceDIR[flxmlrpc]=$projectDir/flxmlrpc-${flxmlrpcVer}
sourceDIR[hamlib]=$projectDir/hamlib-${hamlibVer}
sourceDIR[flrig]=$projectDir/flrig-${flrigVer}
sourceDIR[fldigi]=$projectDir/fldigi-${fldigiVer}


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

for i in $(echo ${programName[@]}); do
  thisProgram=${i}
  thisSourceURL=${sourceURL[$thisProgram]}
  thisSourceTAR=${sourceTAR[$thisProgram]}
  echo -e "Program..............................: ${thisProgram}"
  echo -e "Source URL...........................: ${thisSourceURL}"
  echo -e "Source TAR...........................: ${thisSourceTAR}"
  get_source_tar ${thisSourceURL} ${thisSourceTAR} ${thisProgram}
done

popd
#
# Enable source repositories
#
if grep "^#deb-src" /etc/apt/sources.list; then
  echo -e "Enable source repositories"
  sudo sed --inplace=.bak 's/^#deb-src/deb-src/g' /etc/apt/sources.list
fi

sudo apt-get --assume-yes install aptitude
sudo aptitude --assume-yes update

if [[ ! -f /usr/include/X11/Xft/Xft.h ]]; then
  echo "no Xft.h file found --bailing out"
  exit 1
fi
#
# Increase Swap Size
#
swapSizeOld=`grep "CONF_SWAPSIZE=" /etc/dphys-swapfile`
swapSizeNew="CONF_SWAPSIZE=1024"
if [[ $swapSizeNew != $swapSizeOld ]]; then
  echo -e "Increase Swap Size"
  sudo sed --inplace=.bak "s/$swapSizeOld/$swapSizeNew/g" /etc/dphys-swapfile
  sudo /etc/init.d/dphys-swapfile stop
  sudo /etc/init.d/dphys-swapfile start
fi
free -m
#
# Compile Programs
#
for i in $(echo ${programName[@]}); do
  thisProgram=${i}
  thisSourceDIR=${sourceDIR[$thisProgram]}
  echo -e "Program..............................: ${thisProgram}"
  echo -e "Source DIR...........................: ${thisSourceDIR}"
  compile_source ${thisSourceDIR}
done
#
# install Volume Manager
#
sudo aptitude --assume-yes install pavucontrol
#
# Enable Dial:
#
sudo adduser pi dialout
