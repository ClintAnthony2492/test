import input_commands as command
import pyb
import os
import machine

pyb.LED(4).toggle()
command.send_command("standby")

os.remove("GPGGA.csv")
os.remove("GPGSA.csv")
os.remove("GPGSV.csv")
os.remove("GPRMC.csv")
os.remove("GPVTG.csv")

