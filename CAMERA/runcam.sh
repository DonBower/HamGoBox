#!/bin/bash
BASEDIR="/mnt/usbstick/pictures"
while true; do
	DATE=$(date +"%Y-%m-%d_%H-%M-%S")
	#raspistill -n -vf -hf -o $BASEDIR/$DATE.jpg
	raspistill --annotate 12 --annotateex 16,0xff,0x808000 --preview 740,40,540,320 --timeout 4000 --vflip --hflip --output $BASEDIR/$DATE.jpg
	sleep 1s
done
