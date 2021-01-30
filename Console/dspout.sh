#!/bin/bash
sleep 10
if [[ -f /home/pi/dspout.errlog.txt ]]; then
  rm /home/pi/dspout.errlog.txt
fi

/home/pi/Developer/Console/dspout.py > /dev/tty1 &
