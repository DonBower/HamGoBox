#!/usr/bin/python3
import os
from os import path
import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta


xmlFile = '/tmp/solarrss.xml'

def getRSS(xmlFile):
    # url of rss feed
    url = 'http://www.hamqsl.com/solarrss.php'
    # creating HTTP response object from given url
    resp = requests.get(url)
    # saving the xml file
    with open(xmlFile, 'wb') as f:
        f.write(resp.content)

def bandIndex(thisBand):
    switcher={
        '80m-40m':0,
        '30m-20m':1,
        '17m-15m':2,
        '12m-10m':3
        }
    return switcher.get(thisBand,"Invalid Band")

def timeIndex(thisTime):
    switcher={
            'day':0,
            'night':1
         }
    return switcher.get(thisTime,"Invalid Time")

def parseRSS(xmlFile):
    global thisMUF, theseConditions
    # create element tree object
    tree = ET.parse(xmlFile)
    # get root element
    root = tree.getroot()
    solarData = root.findall('./channel/item/solar/solardata')
    thisMUF=root.findall('./channel/item/solar/solardata/muf')[0].text
    # create empty list for news items
    theseConditions = [['' for x in range(4)] for y in range(2)]
    # iterate news items
    for band in root.findall('./channel/item/solar/solardata/calculatedconditions/band'):
        thisBand=band.attrib['name']
        thisTime=band.attrib['time']
        thisCondition=band.text
        theseConditions[timeIndex(thisTime)][bandIndex(thisBand)] = thisCondition

def printSolar():
    print(f'MUF={thisMUF:5s}|80m-40m|30m-20m|17m-15m|12m-10m                    '[:40])
    print(f'Day      |{theseConditions[0][0]:7s}|{theseConditions[0][1]:7s}|{theseConditions[0][2]:7s}|{theseConditions[0][3]:7s}                    '[:40])
    print(f'Night    |{theseConditions[1][0]:7s}|{theseConditions[1][1]:7s}|{theseConditions[1][2]:7s}|{theseConditions[1][3]:7s}                    '[:40])

if not path.exists(xmlFile) or now > freshDate:
    print('getRSS()')

getRSS(xmlFile)
loadRSS(xmlFile)
parseRSS(xmlFile)
printSolar()
