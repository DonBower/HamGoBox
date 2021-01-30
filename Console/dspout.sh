#!/bin/bash
sleep 15
if [[ -f /home/pi/dspout.py.errlog.txt ]]; then
  rm /home/pi/dspout.py.errlog.txt
fi

/home/pi/Developer/HamGoBox/Console/dspout.py > /dev/tty1 2> /home/pi/dspout.py.errlog.txt &
