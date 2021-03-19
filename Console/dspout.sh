#!/bin/bash
sleep 10
if [[ -f /home/pi/dspout.py.errlog.txt ]]; then
  rm /home/pi/dspout.py.errlog.txt
fi

touch /home/pi/gitpull.log
chmod 666 /home/pi/gitpull.log

date >> /home/pi/gitpull.log

while true; do
  if ps -ef | grep dspout.py | grep --quiet -v grep; then
    sleep 10
  else
    pushd /home/pi/Developer/HamGoBox

    if nc -tv -w 10 github.com 443; then
      git pull >> /home/pi/gitpull.log 2>&1
    else
      echo github not avaiable >> /home/pi/gitpull.log 2>&1
    fi

    popd

    /home/pi/Developer/HamGoBox/Console/dspout.py > /dev/tty1 2> /home/pi/dspout.py.errlog.txt &
  fi
done
