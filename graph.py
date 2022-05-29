# imports
import matplotlib.pyplot as plt
from time import localtime, strftime, mktime, time
from glob import glob
from os import path
from datetime import datetime as dt

# ingest function: takes given array of csv entries and separates into three lists before returning with proper labels
def ingest(given):

    # breaks all lines down into individual lists and converts them back to numbers
    stamp = []
    one = []
    two = []
    for i in given:
        e = i.split(',')

        stamp.append(int(e[0]))
        one.append(float(e[1]))
        two.append(float(e[2]))

    # finds which probe has higher average and assigns hot and cold label
    oneone = sum(one) / len(one)
    twoone = sum(two) / len(two)

    hot = one if oneone >= twoone else two
    cold = one if oneone <= twoone else two

    # returned processed arrays in a dictionary with hot/cold label assigned
    return {"minimum": min(one + two), "maximum": max(one + two), "time": stamp, "hot": hot, "cold": cold}

# plotting function: takes passed dictionary with process data and creates graph using matplotlib then saves image
def plot(passed):
    # passes plot data for both graphs along with color & name labels
    plt.plot(passed["time"], passed["cold"], label='Cold', color='Blue')
    plt.plot(passed["time"], passed["hot"], label='Hot', color='Red')
    plt.xlabel('Time')
    plt.ylabel('Temp (C)')

    # create custom x-axis major ticks spaced 5 hours apart
    w = [rear_hour]
    inc = 3600 * 5
    for i in range(5):
        w.append(w[i] + inc)

    # build labels for x-axis ticks
    labels = [strftime("%H:%M", localtime(m)) for m in w]

    # set custom ticks and labels on x-axis
    plt.xticks(w, labels)

    # show minor ticks
    plt.minorticks_on()

    # display grid lines of major ticks on x and y axis
    plt.grid()

    # limit x-axis to between first and last major tick
    plt.xlim(w[0],w[-1])

    # limit y-axis between min and max temp (with spacing of 0.5 degree for looks)
    plt.ylim(passed["minimum"] - 0.5, passed["maximum"] + 0.5)

    # saves graph as jpg image (currently named day.jpg)
    plt.savefig("day.jpg", dpi=300)

def delta(passed):
    d = []
    for v in range(len(passed['hot'])):
        d.append(passed['hot'][v] - passed['cold'][v])

    plt.plot(passed['time'], d,label='Delta', color='grey')
    plt.xlabel('Time')
    plt.ylabel('Temp (C)')

    # create custom x-axis major ticks spaced 5 hours apart
    w = [rear_hour]
    inc = 3600 * 5
    for i in range(5):
        w.append(w[i] + inc)

    # build labels for x-axis ticks
    labels = [strftime("%H:%M", localtime(m)) for m in w]

    # set custom ticks and labels on x-axis
    plt.xticks(w, labels)

    # show minor ticks
    plt.minorticks_on()

    # display grid lines of major ticks on x and y axis
    plt.grid()

    # limit x-axis to between first and last major tick
    plt.xlim(w[0], w[-1])

    # saves graph as jpg image (currently named day.jpg)
    plt.savefig("delta.jpg", dpi=300)

if __name__ == '__main__':
    # adds 5 minutes to current time
    x = time() + 300

    # creates datetime timestamp from +5 minute time an breaks into year, month, day, hour
    s = dt.fromtimestamp(x)
    year = s.year
    month = s.month
    day = s.day
    hour = s.hour

    # rebuilds new datetime timestamp from broken out values
    q = dt(year=year, month=month, day=day, hour=hour)

    # turns datetime timestamp into unix timestamp
    tu = dt.timetuple(q)

    # makes timestamp into int
    ts = int(mktime(tu))

    # removes 24 hours (86400 seconds) from unix timestamp
    rear_hour = ts - 86400


    # finds all files matching name pattern for log file using glob
    search = glob('logs/temp_log-*')

    # sort files by creation time oldest to newest
    search.sort(key=path.getmtime)

    # opens newest file and dumps all lines to an array
    with open(search[-1], "r") as f:
        t = f.readlines()

    while True:
        if int(t[1].split(',')[0]) <= rear_hour:
            del t[0]  # removes header
            take = ingest(t)  # pass file data to ingest function to process for plotting

            # pass processed data to plotting function
            plot(take)
            # reset/ clear plot data for delta function
            plt.clf()
            # create and plot temp delta to separate graph
            delta(take)

            # break from loop and terminate script
            break
        else:
            del search[-1]  # removes last entry in file listing

            with open(search[-1], 'r') as g:  # reads new last entry
                tt = g.readlines()

            del t[0]  # remove header from first list
            t.insert(0, tt[0])  # replace with new header
            del tt[0]  # remove header from new list

            for z in range(len(tt)):
                t.insert(1, tt[-1])
                del tt[-1]