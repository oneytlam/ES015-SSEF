# This code receives inputs from the serial monitor of ESP8266.
# Ran on a MacBook Air 2017.

import serial
import time

ser = serial.Serial("/dev/cu.usbserial-0001", baudrate=115200, timeout=.1)

##while 1:
##    byte = ser.read(size=8)
##    print(byte)

while True:
    thing = ser.readline()
    print(thing)

##def write_read(x):
##    arduino.write(bytes(x, 'utf-8'))
##    time.sleep(0.05)
##    data = arduino.readline()
##    return data


##while True:
##    num = input("Enter a number: ")
##    value = write_read(num)
##    print(value)