# main.py -- put your code here!
import time
import pyb
from pyb import UART
from micropyGPS import MicropyGPS

# Setup the connection to your GPS here
# This example uses UART 3 with RX on pin Y10
# Baudrate is 9600bps, with the standard 8 bits, 1 stop bit, no parity
uart = UART(4, 9600)

# Instatntiate the micropyGPS object
my_gps = MicropyGPS(-7)

# Continuous Tests for characters available in the UART buffer, any characters are feed into the GPS
# object. When enough char are feed to represent a whole, valid sentence, stat is set as the name of the
# sentence and printed

array1 = [1,2,3]

time_duration = 10 #seconds
start_time = time.time()
t_end = time.time() + time_duration

pyb.LED(3).toggle()

while time.time() < t_end:
    if uart.any():
        stat = my_gps.update(chr(uart.readchar())) # Note the conversion to to chr, UART outputs ints normally
        if stat: 
            elapsed_time = time.time()  - start_time
            gps_segs = my_gps.gps_segments
            gps_segs.insert(0, elapsed_time) 
            gps_segs = str(gps_segs)
            gps_segs = gps_segs.replace('[', '')
            gps_segs = gps_segs.replace(']', '')
            print (gps_segs)
            stat = None
