#!/bin/bash
clear
echo ">>>>>Kill DSPOUT<<<<<<< "
sh=`ps -ef | grep dspout.sh | grep errlog | awk '{print $2}'`
py=`ps -ef | grep dspout.py | grep errlog | awk '{print $2}'`
sudo kill -9 ${sh}
sleep 1
sudo kill -9 ${py}
sleep 1
clear