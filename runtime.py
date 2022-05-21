# imports
from glob import glob
from time import time, localtime, sleep

# time between data pull in minutes
checkTime = 5

# number of pulls kept, default is 24 hours with given checkTime
# can be any int
# +1 accounts for header
keep = ((60/checkTime) * 24) + 1

# reads most recent data from sensor, converts to C and returns
def reader(given):
    # opens probe read vector and dumps contents to array
    with open(given, 'r') as f:
        lines = f.readlines()

    # strips extra data from array and pulls data as millicelsius
    workingVal = float(lines[1][-6:])

    # converts millicelsius to celsius
    tempC = workingVal/1000

    # returns temperature data for the probe in celsius rounded to the 100th
    return round(tempC, 2)

if __name__ == '__main__':
    # finds and prepares one wire devices devices
    base_path = '/sys/bus/w1/devices/'
    dev_search = glob(base_path + '28*')

    # assigns found probes to variables and appends with read vector
    probe1 = dev_search[0] + '/w1_slave'
    probe2 = dev_search[1] + '/w1_slave'

    print("Temp probes initialized")

    # creates JSON log file
    timestamp = localtime()
    filename = f'logs/temp_log-{timestamp[1]}_{timestamp[2]}_{timestamp[0]}_{timestamp[3]}_{timestamp[4]}.csv'

    with open(filename, 'w') as file:
        file.write(f"{int(round(time(), 0))},probe 1,probe 2\n")

    print("log file made")

    # checkTime minutes to seconds
    checkSec = checkTime * 60
    while True:
        # reads data from probes using reader function and assigns returned values to variables
        one = reader(probe1)
        two = reader(probe2)

        # appends data directly to csv file
        with open(filename, 'a') as g:
            g.write("{},{},{}".format(int(round(time(),0)), one, two) + '\n')

        sleep(checkSec)