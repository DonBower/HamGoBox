#!/bin/bash
sleep 20
if [[ -f /home/pi/dspout.py.errlog.txt ]]; then
  rm /home/pi/dspout.py.errlog.txt
fi

while true; do
  if ps -ef | grep dspout.py | grep --quiet -v grep; then
    sleep 10
  else
    /home/pi/Developer/HamGoBox/Console/dspout.py > /dev/tty1 2> /home/pi/dspout.py.errlog.txt &
  fi
done
