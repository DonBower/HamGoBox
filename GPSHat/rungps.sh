#!/bin/bash
inputDevice=/dev/ttyAMA0
#inputDevice=/Users/don/Developer/Eclipse2017/gpststdta.txt
IFS=":"
BASEDIR="/mnt/usbstick"
#BASEDIR="/Users/don/Developer/Eclipse2017"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE=$BASEDIR/gpslog.txt
RAWFILE=$BASEDIR/rawgps/gpsraw-$DATE.txt
DATAFILE=$BASEDIR/data/gpsdata-$DATE.txt

dateStamp=$(date +"%Y-%m-%d")
echo $dateStamp "Start GPS Process" >> $LOGFILE

echo -e "inputDevice is $inputDevice"

function extract_dms() {
degrees_mf=`echo $1 | cut -d '.' -f 1`
if [[ ${#degrees_mf} -eq 5 ]]; then
  deg=${1:0:3}
  min=${1:3:2}
  s=${1:6:4}
else
  deg=${1:0:2}
  min=${1:2:2}
  s=${1:5:4}
fi
sec=$(echo "scale=4; $s/10000 * 60" | bc)
}

function dms_to_dd() {
  dd=`echo "scale=6; $1 + $2/60 + $3/3600" | bc`
}



while [ True ]
  do
      read this_line

      # if cr/lf bothers you, make it lf only
      # (os-specfic concern)
      #
      this_line=$( echo $this_line | sed s/$'\r'//g )
      # get a precise time stamp
      # %N = nanoseconds
      #
      timeStamp=$(date +"%H:%M:%S.%N")

      echo $timeStamp $this_line >> $RAWFILE
      gps_sentance=$(echo $this_line | cut -d, -f 1)
      gps_chksum=$(echo $this_line | cut -d, -f 15 )
      if [ ${#gps_chksum} == 3 ]; then
        gps_chksum_star=$(echo $this_line | cut -d, -f 15 | cut -c1)
      else
        gps_chksum_star=$(echo $this_line | cut -d, -f 15 | cut -c5)
      fi
      #
      # let us filter the current position
      #
      #  echo -e "GPS Sentance is ${gps_sentance}"
      #  echo -e "Checksum is ${gps_chksum}"
      #  echo -e "Checksum Star is ${gps_chksum_star}"
  	if [[ ${gps_sentance} == "\$GPGGA" && ${gps_chksum_star} == "*" ]]
    	then
        gps_time=$(echo $this_line | cut -d, -f 2)
        gps_latdeg=$(echo $this_line | cut -d, -f 3)
        gps_latdir=$(echo $this_line | cut -d, -f 4)
        gps_londeg=$(echo $this_line | cut -d, -f 5)
        gps_londir=$(echo $this_line | cut -d, -f 6)
        gps_fix=$(echo $this_line | cut -d, -f 7)
        gps_sats=$(echo $this_line | cut -d, -f 8)
        gps_hdop=$(echo $this_line | cut -d, -f 9)
        gps_elev=$(echo $this_line | cut -d, -f 10)
        gps_elevscale=$(echo $this_line | cut -d, -f 11)

        extract_dms $gps_latdeg
        #printf "extract_dms returned %03i° %02i\' %02.2f\"\n" $deg $min $sec
        lat_d=$deg
        lat_m=$min
        lat_s=$sec
        dms_to_dd $lat_d $lat_m $lat_s
        #printf "dms_to_dd returned %03.6f\n" $dd
        lat_dd=$dd

        extract_dms $gps_londeg
        #printf "extract_dms returned %03i° %02i\' %02.2f\"\n" $deg $min $sec
        lon_d=$deg
        lon_m=$min
        lon_s=$sec
        dms_to_dd $lon_d $lon_m $lon_s
        #printf "dms_to_dd returned %03.6f\n" $dd
        lon_dd=$dd

        timeStamp=$(date +"%H:%M:%S")
        printf "%8s %8s %2.6f %1s %3.6f %1s% 4.1f %1s\n" "$dateStamp" "$timeStamp" $lat_dd "$gps_latdir" $lon_dd "$gps_londir" $gps_elev $gps_elevscale
        printf "%8s %8s %2.6f %1s %3.6f %1s% 4.1f %1s\n" "$dateStamp" "$timeStamp" $lat_dd "$gps_latdir" $lon_dd "$gps_londir" $gps_elev $gps_elevscale >> $DATAFILE
        sleep 5s
  	fi

done < $inputDevice
