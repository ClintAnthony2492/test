"""
This python script ...
"""
import time
from time import sleep
from micropyGPS import MicropyGPS
import pyb
import input_commands as command
from pyb import UART
import machine



# Setup the connection to your GPS here
# This example uses UART 3 with RX on pin Y10
# Baudrate is 9600bps, with the standard 8 bits, 1 stop bit, no parity
UART = UART(4, 9600)

# Instatntiate the micropyGPS object
MY_GPS = MicropyGPS(-7)

# Global Variables
ARR_GPVTG = []
ARR_GPGGA = []
ARR_GPGSA = []
ARR_GPRMC = []
ARR_GPGSV = []
FIX_DATA = "no_fix"

#function parse_messages()
def parse_messages():
    if UART.any():
        stat = MY_GPS.update(chr(UART.readchar()))
        if stat:
            elapsed_time = time.time() - START_TIME
            gps_segs = MY_GPS.gps_segments
            gps_segs.insert(0, elapsed_time)
            gps_segs = str(gps_segs)
            gps_segs = gps_segs.replace('[', '')
            gps_segs = gps_segs.replace(']', '')
            print(gps_segs)

            if stat == "GPVTG":
                global ARR_GPVTG
                ARR_GPVTG.append(gps_segs)

            if stat == "GPGGA":
                global ARR_GPGGA
                ARR_GPGGA.append(gps_segs)
                if int(MY_GPS.gps_segments[7]) > 0:
                    global FIX_DATA
                    FIX_DATA = "fix"

            if stat == "GPGSA":
                global ARR_GPGSA
                ARR_GPGSA.append(gps_segs)

            if stat == "GPRMC":
                global ARR_GPRMC
                ARR_GPRMC.append(gps_segs)

            if stat == "GPGSV":
                global ARR_GPGSV
                ARR_GPGSV.append(gps_segs)

            stat = None


def create_log():
    #function create_log()
    global ARR_GPVTG
    global ARR_GPGGA
    global ARR_GPGSA
    global ARR_GPRMC
    global ARR_GPGSV

    file_gpvtg = open("GPVTG.csv", "a")
    file_gpgga = open("GPGGA.csv", "a")
    file_gpgsa = open("GPGSA.csv", "a")
    file_gprmc = open("GPRMC.csv", "a")
    file_gpgsv = open("GPGSV.csv", "a")

    for sentence in ARR_GPVTG:
        file_gpvtg.write(sentence)
        file_gpvtg.write("\n")
        sleep(0.10)
    print("GPVTG parse complete")

    for sentence in ARR_GPGGA:
        file_gpgga.write(sentence)
        file_gpgga.write("\n")
        sleep(0.10)
    print("GPGGA parse complete")

    for sentence in ARR_GPGSA:
        file_gpgsa.write(sentence)
        file_gpgsa.write("\n")
        sleep(0.10)
    print("GPGSA parse complete")

    for sentence in ARR_GPRMC:
        file_gprmc.write(sentence)
        file_gprmc.write("\n")
        sleep(0.10)
    print("GPRMC parse complete")

    for sentence in ARR_GPGSV:
        file_gpgsv.write(sentence)
        file_gpgsv.write("\n")
        sleep(0.10)
    print("GPGSV parse complete")

    file_gpvtg.close()
    file_gpgga.close()
    file_gpgsa.close()
    file_gprmc.close()
    file_gpgsv.close()

if __name__ == '__main__':
    NAVIGATION_TIME_DURATION = 10 #5 seconds
    START_TIME = time.time()

    command.send_command("cold_start")

    pyb.LED(1).on() #Turn on Red LED: GPS Module is in ACQUISITION MODE

    while FIX_DATA == "no_fix":
        parse_messages()

    print("GPS FIX: GPS Satallites and Navigation Acquired...")

    pyb.LED(1).off()
    pyb.LED(2).on()

    T_END = time.time() + NAVIGATION_TIME_DURATION
    while time.time() < T_END:
        parse_messages()

    command.send_command("standby")
    
    create_log()
    sleep(3.0)
    machine.reset()
