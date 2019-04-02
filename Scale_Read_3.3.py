import serial
import time
from time import gmtime, strftime, localtime
import datetime

#Setting Values
print("\nWelcome to the serial read and record program. \n\nPlease enter integer values only for the following options.")
interval =  int(input("How many samples per minute? (20 max): "))
timeframe = ((int(input("How many hours would you like to record over?: "))) * 60)
filename = input("Please name log file: \n")

def checkValues(x):
    if (x > 20) or (60 % x != 0):
        print("Sorry, interval must be less than or equal to 20, and must be a divisor of 60.")
        interval =  int(input("How many samples per minute? (20 max): "))


checkValues(interval)

#time in seconds & minutes
s_time = int(time.time())
m_time = s_time / 60


#Opening Serial Port and log file
s = serial.Serial('COM4', 300, bytesize=8)
file = open(filename + ".txt", "w")

#Printing date and time
Time = (strftime("Date: %x  \nTime: %X  "  , localtime()))
print(Time)

#Writing file header
file.write(str(Time) + "\n\n" + '"Time","Weight"\n')

#Defining serial reading function
def StartRead():
    while True:
        start = s.read()
        if start == b'\x00':
            res = s.read(13)
            val = float(str(res)[3:12])
            print(val)
            file.write(str(round((time.time() - Start_Time), 15))[0:15] + "," + str(val) + "\n")
            return(val)
            
#Defining function to read at set interval
def atInterval():
    count = 0
    Time = (strftime("%X", gmtime()))
    if interval == 1:
        if (int(Time[6:8]) == 0) and (count == 0):
            print(time.time() - Start_Time)
            StartRead()
            count += 1
        if (int(Time[6]) == 1):
            count = 0
    if interval > 1:
        if ((int(Time[6:8])) == 0 or ((int(Time[6:8]) % (60 / interval)) == 0)) and count == 0:
            print(time.time() - Start_Time)
            StartRead()
            count += 1
        if ((int(Time[6:8]) % (60 / interval))) != 0:
            count = 0


#Setting variable to see if the loop has already run once during a second            
looptime = (time.time() + 1)
Start_Time = time.time()

#Looping the function until the specified timespan has passed
while True:
    s.read(13)
    if (int(time.time()) / 60) < (m_time + timeframe) and (time.time() >= (looptime + 1)):
        inTime = 1
        atInterval()
        looptime = time.time()
    if (int(time.time()) / 60) > (m_time + timeframe):
        print("\nDone recording. File output:\n")
        inTime = 0
        s.close()
        file.close
        file = open(filename + ".txt","r")
        print(file.read())
        file.close
        break
        
                                     


