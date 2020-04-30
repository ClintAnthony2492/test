import os

class globals:
    ttff = 0

def print_header():
    print ("\n\n-----------------------------------------------------------------------------")
    print ("-- Post-Processing and Analysis Results--------------------------------------")
    print ("-----------------------------------------------------------------------------\n")

    print ("(Test data was parse from the first GPS Sentence after GPS had its first fix)\n")

def print_closer():
    print ("\n-----------------------------------------------------------------------------")
    print ("-- End of Post-Processing and Analysis Results ------------------------------")
    print ("-----------------------------------------------------------------------------\n\n")

def format_date(date):

    # This if state is for robustness that accomadate dates such as: 
    # - 150520 (May 15, 2020)
    # - 51119 (November 5, 2020)
    date_str = str(date)
    if len(date_str) < 6:
        date_str = ("0" + str(date))

    day = date_str[0] + date_str[1]
    month = date_str[2] + date_str[3]
    year = date_str[4] + date_str[5]

    if month == "01":
        month = "January"
    elif month == "02":
        month = "February"
    elif month == "03":
        month = "March"
    elif month == "04":
        month = "April"
    elif month == "05":
        month = "May"
    elif month == "06":
        month = "June"
    elif month == "07":
        month = "July"
    elif month == "08":
        month = "August"
    elif month == "09":
        month = "September"
    elif month == "10":
        month = "October"
    elif month == "11":
        month = "November"
    elif month == "12":
        month = "December"

    if int(year) <= 20:
        year = "20" + year
    else :
        year = "19" + year

    return (month + " " + day + ", " + year)

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

    print ("\n\n|---------- GPGGA Sentence: Satellite Status ----------|\n")
    print(" Time to First Fix:                  " + str(GLOBAL_VARS.ttff))
    print(" Longitude:                          " + str(lon))
    print(" Latitude:                           " + str(lat))
    print(" Number of Satellites Used:          " + str(num_of_sats))
    print(" Horizontal Dilution of Position:    " + str(hdop))
    print(" Altitude (m):                       " + str(alt))
    print(" Geoid Height:                       " + str(geoid_height))
    print ("\n|------------------------------------------------------|\n\n")

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
                fix_type = "1 = No Fix"
            if fix == 2:
                fix_type = "2 = 2D Fix"
            if fix == 3: 
                fix_type = "3 = 3D Fix"

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

    sats_str = str(sats)
    sats_str = sats_str.replace("[", '') 
    sats_str = sats_str.replace("]", '') 

    print ("\n\n|----- GPGSA Sentence: Global Positioning System Fix Data -----|\n")
    print(" Fix Type:                           " + str(fix_type))
    print(" Number of Satellites in View:       " + str(sats_str))
    print(" Dilution of Precision:              " + str(pdop))
    print(" Horizontal Dilution of Precision:   " + str(hdop))
    print(" Vertical Dilution of Precision:     " + str(vdop))
    print ("\n|--------------------------------------------------------------|\n\n")

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
            if int(data[index][2]) == 2:
                num_of_sats_in_view = int(data[index][4])
                for sat_index in range(5, 21):
                    sat_info.append(data[index][sat_index])
                for sat_index in range(5, ((num_of_sats_in_view % 4) * 4 + 5)):
                    sat_info.append(data[index+1][sat_index])

                break
        index += 1

    sat_index = 0;
    print ("\n\n|----------- GPGSV Sentence: Satellites in View -----------|\n")
    print(" Number of Satellites in View:       " + str(num_of_sats_in_view))
    while sat_index < len(sat_info):
        print ("\n Satellite PRN number:              " + sat_info[sat_index])
        print (" Azimuth (deg):                     " + sat_info[sat_index+1])
        print (" Signal to Noise Ratio (SNR):       " + sat_info[sat_index+2])
        print (" Elevation (deg):                   " + sat_info[sat_index+3])
        sat_index += 4
    print ("\n|----------------------------------------------------------|\n\n")

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

    print ("\n\n|----- GPRMC Sentence: Recommended Minimum sentence C -----|\n")
    print(" Latitude:                           " + str(lat))
    print(" Latitude:                           " + str(lon))
    print(" Speed Over the Ground (knots):      " + str(speed_over_ground))
    print(" Track Angle (deg):                  " + str(track_angle))
    print(" Date:                               " + format_date(date))
    print ("\n|-----------------------------------------------------------|\n\n")

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

    print ("\n\n|---- GPVTG Sentence: Track Made Good and Ground Speed -----|\n")
    print(" True Track Made Good (deg):         " + str(true_track))
    print(" Ground speed (knots):               " + str(ground_speed_knots))
    print(" Ground speed (kph):                 " + str(ground_speed_knots))
    print ("\n|-----------------------------------------------------------|\n\n")

def TTFF_test():
    
    test_results = 'FAIL'

    if GLOBAL_VARS.ttff < 60:
        test_results = 'PASS'

    print ("\n\n|~~~~~~~~~~~~ Test Results: Time to First Fix: ~~~~~~~~~~~~|\n")
    print (" TTFF                                       " + str(GLOBAL_VARS.ttff) + " seconds")
    print (" Test Results (TTFF under 60 seconds)       " + test_results)
    print ("\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\n\n")

if __name__ == '__main__':
    GLOBAL_VARS = globals()
    print_header()
    pp_gpgga()
    pp_gpgsa()
    pp_gpgsv()
    pp_gprmc()
    pp_gpvtg()
    TTFF_test()
    print_closer()


