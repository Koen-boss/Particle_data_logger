import serial
import time
from datetime import datetime
import os
from multiprocessing import Process

#importing helper files:
from DCCA_Config import DCCA_Processor, DCCA_SetUp, DCCA_IDs
from AHT_Config import AHT_Processor, AHT_IDs
from SBA_Config import SBA_Processor, SBA_IDs

#setup:
DCCA_SetUp()

#starting serial 
ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1) #intitializing serial
time.sleep(2) #waiting for serial to start

#main loop
while True:
    #check for incoming serial
    if ser.in_waiting >0:
        line = ser.readline().decode('utf-8', errors = 're' \
        'place').strip()
        print("received", line)
        try:
            dataArray = line.split("|") #data format [event name, event data]
            eventName = dataArray[0].removeprefix("dataLog_").strip() #split off the "dataLog" indicator
            eventData = dataArray[1]
            print(eventName)
            print(eventData)
            print(repr(eventName))
            #Sending data for designated processor based on device ID
            match eventName:
                case n if n in DCCA_IDs:
                    DCCA_Processor(eventName, eventData)
                case n if n in AHT_IDs:
                    AHT_Processor(eventName, eventData)
                case n if n in SBA_IDs:
                    SBA_Processor(eventName, eventData)
                case _:
                    print("Product ID not recognised")
        except:
            print("Error: Data received doesn't match data structure")