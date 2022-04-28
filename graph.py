# imports
import matplotlib.pyplot as plt
from time import localtime, strftime
from glob import glob
from os import path
# from runtime import keep

# ingest function: takes given array of csv entries and separates into three lists before returning with proper labels
def ingest(given):

    # breaks all lines down into individual lists and converts them back to numbers
    time = []
    one = []
    two = []
    for i in given:
        e = i.split(',')

        time.append(int(e[0]))
        one.append(float(e[1]))
        two.append(float(e[2]))

    # finds which probe has higher average and assigns hot and cold label
    oneone = sum(one) / len(one)
    twoone = sum(two) / len(two)

    hot = one if oneone >= twoone else two
    cold = one if oneone <= twoone else two

    # returned processed arrays in a dictionary with hot/cold label assigned
    return {"minimum": min(one + two), "maximum": max(one + two), "time": time, "hot": hot, "cold": cold}

# plotting function: takes passed dictionary with process data and creates graph using matplotlib then saves image
def plot(passed):
    # create axis object assignment to manipulate axis labeling later.
    a = plt.axes()

    # passes plot data for both graphs along with color & name labels
    plt.plot(passed["time"], passed["cold"], label='Cold', color='Blue')
    plt.plot(passed["time"], passed["hot"], label='Hot', color='Red')
    plt.xlabel('Time')
    plt.ylabel('Temp (C)')
    plt.legend()
    plt.title('Test Graph')

    # set x-axis with custom tick spacing based (currently) on first, middle, last
    holding = [passed["time"][0], passed["time"][int(len(passed["time"]) / 2)], passed["time"][-1]]
    a.set_xticks(holding)

    # assign hour:minute labels to x-ticks based on assignment above
    a.set_xticklabels([strftime("%H:%M", localtime(m)) for m in holding])

    # saves graph as jpg image (currently named output.jpg)
    plt.savefig("output.jpg", dpi=300)

''' 
idea: if newest file does not have 24 hours of data (using the 5 minute pull time math, 288 entries + one header line) grab the next oldest file and combine
'''

if __name__ == '__main__':

    # finds all files matching name pattern for log file using glob
    search = glob('temp_log-*')
    # sort files by creation time oldest to newest
    search.sort(key=path.getmtime)

    # opens newest file and dumps all lines to an array
    with open(search[-1], "r") as f:
        t = f.readlines()

    if len(t) == 289:  # keep:
        del t[0]  # removes header
        take = ingest(t)  # pass file data to ingest function to process for plotting
        plot(take)  # pass processed data to plotting function

    else:
        print('to short: ', len(t))