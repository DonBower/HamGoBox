#!/bin/bash
this_line=$GPGGA,050241.000,3401.8807,N,11725.0211,W,2,09,1.21,329.8,M,-32.8,M,0000,0000*53
IFS=":"
dateStamp=$(date +"%Y/%m/%d")
#echo $dateStamp

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

#echo "Lets Convert!"
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
printf "%8s %8s %2.6f %1s %3.6f %1s\n" "$dateStamp" "$timeStamp" $lat_dd "$gps_latdir" $lon_dd "$gps_londir"
