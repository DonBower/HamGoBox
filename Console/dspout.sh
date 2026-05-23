#!/bin/bash
sleep 10
if [[ -f /home/don/dspout.py.errlog.txt ]]; then
  rm /home/don/dspout.py.errlog.txt
fi

touch /home/don/gitpull.log
chmod 666 /home/don/gitpull.log

date >> /home/don/gitpull.log

while true; do
  if ps -ef | grep dspout.py | grep --quiet -v grep; then    
    sleep 10
  else
    printf '\033[3J\033[2J\033[H' > /dev/tty1
    echo "application not running wait 10 seconds" >> /dev/tty1
    sleep 10

    pushd /home/don/Developer/HamGoBox

    if nc -tv -w 10 github.com 443; then
      git pull >> /home/don/gitpull.log 2>&1
    else
      echo github not avaiable >> /dev/tty1
      echo github not avaiable >> /home/don/gitpull.log 2>&1
      sleep 1
    fi

    popd

    /home/don/Developer/HamGoBox/Console/dspout.py > /dev/tty1 2>> /home/don/dspout.py.errlog.txt &
  fi
done
