#import input_commands as command
#import pyb
import os

#command.send_command("standby")
#pyb.LED(3).toggle()

class globals:
    ttff = 0

def get_csv_path(csv_file):
    file = ''
    files = os.listdir('.') 
    for file_name in files:
        if csv_file in file_name and '._' not in file_name:
            file = file_name

    file_path = os.getcwd() + '/' + file
    return (file_path)

def pp_gpgga():
    data = []
    file_path = get_csv_path('GPGGA.csv')
    index = 1

    with open(file_path,'r') as file:
        for line in file:
            line=line.rstrip('\n')
            line=line.rstrip('\r')
            data.append(line.split(','))

    while index < len(data):
        if int(data[index][7]) > 0:
            GLOBAL_VARS.ttff = int(data[index][0])
            lon = (str(data[index][3]) + str(data[index][4])).replace(' ','')
            lat = (str(data[index][5]) + str(data[index][6])).replace(' ','')
            num_of_sats = int(data[index][8])
            hdop = float(data[index][9])
            alt = float(data[index][10])
            geoid_height = float(data[index][12])
            break
        index += 1


    print(GLOBAL_VARS.ttff)
    print(lon)
    print(lat)
    print(num_of_sats)
    print(hdop)
    print(alt)
    print(geoid_height)
    print('\n\n')

def pp_gpgsa():
    data = []
    sats = []
    file_path = get_csv_path('GPGSA.csv')
    index = 1
    prn_index = 4

    with open(file_path,'r') as file:
        for line in file:
            line=line.rstrip('\n')
            line=line.rstrip('\r')
            data.append(line.split(','))

    while index < len(data):
        if int(data[index][0]) > GLOBAL_VARS.ttff:
            fix = int(data[index][3])
            if fix == 1:
                fix_type = "No Fix"
            if fix == 2:
                fix_type = "2D Fix"
            if fix == 3: 
                fix_type = "3D Fix"

            while prn_index < 16:
                if data[index][prn_index] == ' ':
                    break
                else:
                    sats.append(int(data[index][prn_index]))
                prn_index += 1

            pdop = float(data[index][16])
            hdop = float(data[index][17])
            vdop = float(data[index][18])
            break
        index += 1

    print(fix_type)
    print(sats)
    print(pdop)
    print(hdop)
    print(vdop)
    print('\n\n')

def pp_gpgsv():
    data = []
    sat_info = []
    file_path = get_csv_path('GPGSV.csv')
    index = 1

    with open(file_path,'r') as file:
        for line in file:
            line=line.rstrip('\n')
            line=line.rstrip('\r')
            data.append(line.split(','))

    while index < len(data):
        if int(data[index][0]) > GLOBAL_VARS.ttff:
            if int(data[index][2]) == 3:
                num_of_sats_in_view = int(data[index][4])

                for sat_index in range(5, 21):
                    sat_info.append(data[index][sat_index])
                for sat_index in range(5, 21):
                    sat_info.append(data[index+1][sat_index])
                for sat_index in range(5, ((num_of_sats_in_view % 4) * 4 + 5)):
                    sat_info.append(data[index+2][sat_index])

                break
        index += 1


    print(num_of_sats_in_view)
    sat_index = 0;
    while sat_index < len(sat_info):
        print ("Satellite PRN number: " + sat_info[sat_index])
        print ("Azimuth (deg): " + sat_info[sat_index+1])
        print ("Signal to Noise Ratio (SNR): " + sat_info[sat_index+2])
        print ("Elevation (deg): " + sat_info[sat_index+3])
        sat_index += 4
    print('\n\n')

def pp_gprmc():
    data = []
    file_path = get_csv_path('GPRMC.csv')
    index = 1

    with open(file_path,'r') as file:
        for line in file:
            line=line.rstrip('\n')
            line=line.rstrip('\r')
            data.append(line.split(','))

    while index < len(data):
        if int(data[index][0]) > GLOBAL_VARS.ttff:
            lat = (str(data[index][4]) + str(data[index][5])).replace(' ','')
            lon = (str(data[index][6]) + str(data[index][7])).replace(' ','')
            speed_over_ground = float(data[index][8])
            track_angle = float(data[index][9])
            date = int(data[index][10])
            break
        index += 1

    print(lat)
    print(lon)
    print(speed_over_ground)
    print(track_angle)
    print(date)
    print('\n\n')

def pp_gpvtg():
    data = []
    file_path = get_csv_path('GPVTG.csv')
    index = 1

    with open(file_path,'r') as file:
        for line in file:
            line=line.rstrip('\n')
            line=line.rstrip('\r')
            data.append(line.split(','))

    while index < len(data):
        if int(data[index][0]) > GLOBAL_VARS.ttff:
            true_track = float(data[index][2])
            ground_speed_knots = float(data[index][6])
            ground_speed_kph = float(data[index][8])
            break
        index += 1

    print(true_track)
    print(ground_speed_knots)
    print(ground_speed_kph)
    print('\n\n')

GLOBAL_VARS = globals()
pp_gpgga()
pp_gpgsa()
pp_gpgsv()
pp_gprmc()
pp_gpvtg()


