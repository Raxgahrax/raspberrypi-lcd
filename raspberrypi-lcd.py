#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_16x2.py
#  16x2 LCD Test Script
#
# Author : Matt Hawkins, Leon Anavi
# Date   : 06/04/2015
#
# http://www.raspberrypi-spy.co.uk/
# http://anavi.org/
# http://hardware-libre.fr/2013/07/ajouter-un-bouton-dextinction-avec-python/
# Copyright 2015 Matt Hawkins, Leon Anavi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
#--------------------------------------

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

import RPLCD as RPLCD
from RPLCD.gpio import CharLCD
#import
import RPi.GPIO as GPIO
import os
import socket
import fcntl
import struct
import locale
import time
from time import strftime, sleep
from datetime import datetime
import Adafruit_DHT as dht

# Main program block
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])
GPIO.setwarnings(False)
  
def getCPUtemperature():
  res = os.popen("vcgencmd measure_temp").readline()
  return(res.replace("temp=","").replace("'C\n",""))
  
def printDateTime():
  textDate = strftime("%d-%m-%Y", time.localtime())
  textTime = strftime("%H:%M:%S", time.localtime())
  lcd.cursor_pos = (0, 0)
  lcd.write_string(textDate)
  lcd.cursor_pos = (1, 0)
  lcd.write_string(textTime)
  return

def getInterfaceAddress(ifname):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
      s.fileno(),
      0x8915,  # SIOCGIFADDR
      struct.pack('256s', ifname[:15])
    )[20:24])
  except:
    return ''

def getIP():
  ipWlan = getInterfaceAddress('wlan0')
  if ipWlan:
    return ipWlan
  ipEth = getInterfaceAddress('eth0')
  if ipEth:
    return ipEth
	
def printDHT():
  humi, temp = dht.read_retry(dht.DHT22, 21)
  textTemp = 'Temp: %d *C' % temp
  textHumi = 'Humi: %d %%' % humi
  lcd.cursor_pos = (0, 0)
  lcd.write_string(textTemp)
  lcd.cursor_pos = (1, 0)  
  lcd.write_string(textHumi)
  return
  
def main():

  while True:
  
	# Display Time
    index = 0
    while index < 5:
      printDateTime()
      time.sleep(1)
      index += 1

    # Display CPU temperature
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Temperature CPU:")
    textCPU = getCPUtemperature()+" *C"
    lcd.cursor_pos = (1, 0)	
    lcd.write_string(textCPU)
    time.sleep(3)
	
    # Display local IP
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Adresse IP:")
    textIP = getIP()
    lcd.cursor_pos = (1, 0)	
    lcd.write_string(textIP)
    time.sleep(3)
	
	# Display DHT22
    printDHT()
    time.sleep(3)


if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()