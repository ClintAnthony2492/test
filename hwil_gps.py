"""
This python script ...
"""
import time
from time import sleep
from micropyGPS import MicropyGPS
import pyb
import input_commands as command
from pyb import UART

# Setup the connection to your GPS here
# This example uses UART 3 with RX on pin Y10
# Baudrate is 9600bps, with the standard 8 bits, 1 stop bit, no parity
UART = UART(4, 9600)

# Instatntiate the micropyGPS object
MY_GPS = MicropyGPS(-7)

class LogHeaders():
    """This class is needed for the log headers"""
    def __init__(self):
        self.gpvtg_header_str = ''
        self.gpgga_header_str = ''
        self.gpgsa_header_str = ''
        self.gprmc_header_str = ''
        self.gpgsv_header_str = ''

    @staticmethod
    def create_log_headers():
        """This function creates the log headers for each GPS sentence parsed"""
        gpvtg_header = []
        gpgga_header = []
        gpgsa_header = []
        gprmc_header = []
        gpgsv_header = []

        gpvtg_header.append("Elapsed Time, GPS Sentence, True Track Made Good")
        gpvtg_header.append("True True Made Good Type, Magnetic Track Made Good")
        gpvtg_header.append("Magnetic Track Made Good Type, Ground Speed (knots)")
        gpvtg_header.append("Ground Speed Type, Ground Speed (kph), Ground Speed Type")
        gpvtg_header.append("Checksum Type, Checksum")
        LOG.gpvtg_header_str = str(gpvtg_header)
        LOG.gpvtg_header_str = LOG.gpvtg_header_str.replace("'", '')
        LOG.gpvtg_header_str = LOG.gpvtg_header_str.replace('[', '')
        LOG.gpvtg_header_str = LOG.gpvtg_header_str.replace(']', '')

        gpgga_header.append("Elapsed Time, GPS Sentence, Time of Fix Taken (UTC)")
        gpgga_header.append("Latitude, Latitude Direction, Longitude, Longitude Direction")
        gpgga_header.append("Fix Quality, Number of Satallites Tracked, HDOP, Altitude")
        gpgga_header.append("Altitude Type, Height of geoid, Height of Geoid Type, Spare")
        gpgga_header.append("Spare, Checksum")
        LOG.gpgga_header_str = str(gpgga_header)
        LOG.gpgga_header_str = LOG.gpgga_header_str.replace("'", '')
        LOG.gpgga_header_str = LOG.gpgga_header_str.replace('[', '')
        LOG.gpgga_header_str = LOG.gpgga_header_str.replace(']', '')

        gpgsa_header.append("Elapsed Time, GPS Sentence, Auto Select of 2D or 3D (M=Manual), Fix")
        gpgsa_header.append("PRNs of Satallites Used for Fix - Slot1, Slot2, Slot3")
        gpgsa_header.append("Slot4, Slot5, Slot6, Slot7, Slot8, Slot9, Slot10, Slot11, Slot12")
        gpgsa_header.append("PDOP, HDOP, VDOP, Checksum")
        LOG.gpgsa_header_str = str(gpgsa_header)
        LOG.gpgsa_header_str = LOG.gpgsa_header_str.replace("'", '')
        LOG.gpgsa_header_str = LOG.gpgsa_header_str.replace('[', '')
        LOG.gpgsa_header_str = LOG.gpgsa_header_str.replace(']', '')

        gprmc_header.append("Elapsed Time, GPS Sentence, Time of Fix Taken (UTC)")
        gprmc_header.append("Status A=active or V=Void")
        gprmc_header.append("Latitude, Latitude Direction, Longitude, Longitude Direction")
        gprmc_header.append("Speed Over the Ground in Knots, Track angle (deg), Date")
        gprmc_header.append("Magnetic Variation,Magnetic Variation Direction, Checksum")
        LOG.gprmc_header_str = str(gprmc_header)
        LOG.gprmc_header_str = LOG.gprmc_header_str.replace("'", '')
        LOG.gprmc_header_str = LOG.gprmc_header_str.replace('[', '')
        LOG.gprmc_header_str = LOG.gprmc_header_str.replace(']', '')

        gpgsv_header.append("Elapsed Time, GPS Sentence, Number of Sentences, Sentence Number")
        gpgsv_header.append("Number of Satellites in View, Satellite PRN number")
        gpgsv_header.append("Azimuth (deg), SNR, Elevation (deg)")
        gpgsv_header.append("Repeat Up to Four per Sentences,,,,,,,,,,,,Checksum")
        LOG.gpgsv_header_str = str(gpgsv_header)
        LOG.gpgsv_header_str = LOG.gpgsv_header_str.replace("'", '')
        LOG.gpgsv_header_str = LOG.gpgsv_header_str.replace('[', '')
        LOG.gpgsv_header_str = LOG.gpgsv_header_str.replace(']', '')

    @staticmethod
    def test_log_headers():
        """This function test if the log headers are in the right format"""

class GpsParse():
    """This class is the global variables needed"""
    def __init__(self):
        self.the_file = None
        self.arr_gpvtg = []
        self.arr_gpgga = []
        self.arr_gpgsa = []
        self.arr_gprmc = []
        self.arr_gpgsv = []

        self.fix_data = "no_fix"

    @staticmethod
    def parse_gps_sentence():
        """This function parses gps sentences from the GPS module"""
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
                    GPS_PARSE.arr_gpvtg.append(gps_segs)

                if stat == "GPGGA":
                    GPS_PARSE.arr_gpgga.append(gps_segs)
                    if int(MY_GPS.gps_segments[7]) > 0:
                        GPS_PARSE.fix_data = "fix"

                if stat == "GPGSA":
                    GPS_PARSE.arr_gpgsa.append(gps_segs)

                if stat == "GPRMC":
                    GPS_PARSE.arr_gprmc.append(gps_segs)

                if stat == "GPGSV":
                    GPS_PARSE.arr_gpgsv.append(gps_segs)

                stat = None

    @staticmethod
    def generate_logs():
        """This creates log files from the parsed gps sentences and into separate csv files"""

        file_gpvtg = open("GPVTG.csv", "a")
        file_gpgga = open("GPGGA.csv", "a")
        file_gpgsa = open("GPGSA.csv", "a")
        file_gprmc = open("GPRMC.csv", "a")
        file_gpgsv = open("GPGSV.csv", "a")

        LOG.create_log_headers()

        file_gpvtg.write(LOG.gpvtg_header_str)
        file_gpvtg.write("\n")
        file_gpgga.write(LOG.gpgga_header_str)
        file_gpgga.write("\n")
        file_gpgsa.write(LOG.gpgsa_header_str)
        file_gpgsa.write("\n")
        file_gprmc.write(LOG.gprmc_header_str)
        file_gprmc.write("\n")
        file_gpgsv.write(LOG.gpgsv_header_str)
        file_gpgsv.write("\n")

        for sentence in GPS_PARSE.arr_gpvtg:
            file_gpvtg.write(str(sentence).replace("'", ''))
            file_gpvtg.write("\n")
            sleep(0.10)
        print("GPVTG parse complete")

        for sentence in GPS_PARSE.arr_gpgga:
            file_gpgga.write(str(sentence).replace("'", ''))
            file_gpgga.write("\n")
            sleep(0.10)
        print("GPGGA parse complete")

        for sentence in GPS_PARSE.arr_gpgsa:
            file_gpgsa.write(str(sentence).replace("'", ''))
            file_gpgsa.write("\n")
            sleep(0.10)
        print("GPGSA parse complete")

        for sentence in GPS_PARSE.arr_gprmc:
            file_gprmc.write(str(sentence).replace("'", ''))
            file_gprmc.write("\n")
            sleep(0.10)
        print("GPRMC parse complete")

        for sentence in GPS_PARSE.arr_gpgsv:
            file_gpgsv.write(str(sentence).replace("'", ''))
            file_gpgsv.write("\n")
            sleep(0.10)
        print("GPGSV parse complete")

        file_gpvtg.close()
        file_gpgga.close()
        file_gpgsa.close()
        file_gprmc.close()
        file_gpgsv.close()


GPS_PARSE = GpsParse()
LOG = LogHeaders()


if __name__ == '__main__':
    NAVIGATION_TIME_DURATION = 10 #5 seconds

    command.send_command("cold_start")
    #command.send_command("warm_start")

    pyb.LED(1).on() #Turn on Red LED: GPS Module is in ACQUISITION MODE

    START_TIME = time.time()
    while GPS_PARSE.fix_data == "no_fix":
        GPS_PARSE.parse_gps_sentence()

    print("GPS FIX: GPS Satallites and Navigation Acquired...")

    pyb.LED(1).off()
    pyb.LED(2).on()

    T_END = time.time() + NAVIGATION_TIME_DURATION
    while time.time() < T_END:
        GPS_PARSE.parse_gps_sentence()

    command.send_command("standby")
    pyb.LED(2).off()
    pyb.LED(4).on()

    GPS_PARSE.generate_logs()
    sleep(3.0)
