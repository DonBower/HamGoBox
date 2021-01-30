#!/bin/bash
sleep 10
if [[ -f /home/pi/dspout.py.errlog.txt ]]; then
  rm /home/pi/dspout.py.errlog.txt
fi

/home/pi/Developer/Console/dspout.py > /dev/tty1 2> /home/pi/dspout.py.errlog.txt &
