#!/bin/bash
piConsole=/dev/tty1
clear > ${piConsole}
echo "1234567890123456789012345678901234567890" > ${piConsole}
echo "2        1         2         3         4" > ${piConsole}
for i in {1..12}; do
  echo $i > ${piConsole}
done
piConsole=/dev/tty1
clear > ${piConsole}
printf "Timestamp..........: %s\n" "$(date +"%Y-%m-%d %T")" > ${piConsole}
read piSatCount piLat piLon piAltitude < console.gps

#piLat=`cat console.lat`
#piLon=`cat console.lon`
piGrid=`~/HamGoBox/GPSHat/latlon2maiden.py ${piLat} ${piLon}`

printf "Maidenhead.........: %8s   %'06.1fm\n" ${piGrid} > ${piConsole}
printf "Lat/Lon (%02d).......: %07.4f %08.4f\n" ${piSatCount} ${piLat} ${piLon} > ${piConsole}
printf "Altitude...........: %8s   %'06.1fm\n" ${piAltitude} > ${piConsole}
piTempc=`cat console.tempc`
piTempf=`cat console.tempf`
printf "Temp...............: %4.1f°c / %5.1f°f\n" ${piTempc} ${piTempf} > ${piConsole}
piHumidity=`cat console.humidity`
printf "Relitive Humidity..: %5.2f%% \n" ${piHumidity} > ${piConsole}
piPressure=`cat console.hPa`
printf "Pressure...........: %5.2f hPa \n" ${piPressure} > ${piConsole}
