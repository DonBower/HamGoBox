#!/usr/bin/python3
# latlon2maiden  - This script will convert the Latitude and Longitude
# given in decimal, into a maidenhead format
#
# Initalize the script
#
import re,sys,string
errLevel=0
errMsg="\n"
#
# Check for input errors
#
if len(sys.argv) < 3:
    errLevel=errLevel + 1
    errMsg+="You must provide Latitude and Longitude\n"

if len(sys.argv) > 4:
    errLevel=errLevel + 2
    errMsg+="Too Many Arguments.\n"

latitude=float(sys.argv[1])
longitude=float(sys.argv[2])

if latitude < -90 or latitude > 90:
    errLevel=errLevel + 4
    errMsg+="Latitude "
    errMsg+=str(latitude)
    errMsg+=" must be between -90 and 90 degrees\n"

if longitude < -180 or longitude > 180:
    errLevel=errLevel + 8
    errMsg+="Longitude "
    errMsg+=str(longitude)
    errMsg+=" must be between -180 and 180 degrees\n"

if len(sys.argv) == 4: # slob city
    maidenLenght=int(sys.argv[3])
    if maidenLenght<2 or maidenLenght%2!=0:
        errLevel=errLevel + 16
        errMsg+="Persision length requested must be even integer > 0\n"
else:
    maidenLenght=8

if errLevel > 0:
    errMsg+="\nCommand Syntax is latlon2maiden.py {Latitude} {Longitude} [precision | 8]\n"
    sys.stderr.write(errMsg)
    sys.exit(errLevel)

#print(latitude)
#print(longitude)
#print(maidenLenght)

maxMaiden=maidenLenght/2
A=ord('A')

a=divmod(longitude+180,20)
b=divmod(latitude+90,10)
maidenHead=chr(A+int(a[0]))+chr(A+int(b[0]))

longitude=a[1]/2
latitude=b[1]

i=1

while i<maxMaiden:
    i+=1
    a=divmod(longitude,1)
    b=divmod(latitude,1)
    if not(i%2):
        maidenHead+=str(int(a[0]))+str(int(b[0]))
        longitude=24*a[1]
        latitude=24*b[1]
    else:
        tmp=i+1
        tmpString=chr(A+int(a[0]))+chr(A+int(b[0]))
        # Every other set is lowercase
        if not(tmp%4):
            maidenHead+=tmpString.lower()
        else:
            maidenHead+=tmpString
        longitude=10*a[1]
        latitude=10*b[1]

print(maidenHead)
