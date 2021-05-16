#!/bin/bash
cat > /tmp/needed <<CPLIBRARIES
Adafruit-Blinka
adafruit-circuitpython-bmp3xx
adafruit-circuitpython-gps
adafruit-circuitpython-hts221
adafruit-circuitpython-ltr390
adafruit-circuitpython-scd30
adafruit-circuitpython-tsl2591
CPLIBRARIES

i2cdetect -y 1 | \
  tail -n +2 | \
  cut -d ":" -f 2 | \
  sed 's/--//g' | \
  sed 's/ /\n/g' | \
  grep -v ^$ | \
  sed 's/^/0x/g' \
    > /tmp/sensorAddresses


#sudo pip3 list --format json | jq --raw-output '.[] | .name' | grep "^adafruit-circuitpython" > /tmp/installed.tsv

sudo pip3 list --format json | \
  jq --raw-output \
    '.[] |
    [.name, .version] |
    @tsv' | \
  grep --ignore-case \
    --regexp="^adafruit" \
      > /tmp/installed.tsv

while read thisLibrary; do
  thisVersion=`grep --ignore-case --regexp=${thisLibrary} /tmp/installed.tsv | cut -f2`
  if grep --quiet --ignore-case --regexp=${thisLibrary} /tmp/installed.tsv ; then
    echo -e "Upgrade Circuit Python library ${thisLibrary} version ${thisVersion} to latest release"
    sudo pip3 install --upgrade ${thisLibrary}
  else
    echo -e "Install latest release of Circuit Python library ${thisLibrary}"
    sudo pip3 install ${thisLibrary}
  fi
done < /tmp/needed

sudo pip3 list --format json | \
  jq --raw-output \
    '.[] |
    [.name, .version] |
    @tsv' | \
  grep --ignore-case \
    --regexp="^adafruit" \
      > /tmp/upgrade.tsv

clear

echo "The Following Libraries were updated:"
echo ""
diff --side-by-side \
  --suppress-common-lines \
  /tmp/installed.tsv /tmp/upgrade.tsv | \
   awk '{print $4","$2","$5}' > /tmp/upgraded.csv

 echo "Library,From,To" | cat - /tmp/upgraded.csv | csvlook
