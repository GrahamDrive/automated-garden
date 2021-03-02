# Creator: Graham Driver
# Desc: This script is used to track and file all the data recieved by the pi
# for now there are only two sensors tracking air temperature and soil moisture
# level. It is saved to a CSV file and saved as a png as a graph.
import time
from time import strftime, localtime
from csv import reader
import matplotlib.pyplot as plt
from datetime import datetime
import os


def MAIN(temperature, delay, moisture, cputemp):
        cputemp = float(cputemp)
        temperature = float(temperature)
        moisture = float(moisture)
        moisture = 100 - (moisture*100)
        DayMonthYear = str(strftime("%d_%m_%Y", localtime()))
        if os.path.isdir(
                '/Irrigationsystem/Data/{0}'
                .format(DayMonthYear)) is True:
            print('Directory Existed')
        else:
            os.mkdir("/home/pi/Desktop/IrrigationProject/Irrigationsystem/Data/{0}".format(DayMonthYear))
            print("Directory Made")
        d = open("""/Irrigationsystem/Data/{0}/cputemp{0}.csv""".format(str(DayMonthYear)), 'a')
        f = open("""/Irrigationsystem/Data/{0}/temperature_{0}.csv""".format(str(DayMonthYear)), 'a')
        m = open("""/Irrigationsystem/Data/{0}/moisture_{0}.csv""".format(str(DayMonthYear)), 'a')
        if temperature is not None:
            outstring = ('Temp={0:0.1f}* Moisture={1:0.1f}%'
                        .format(temperature, moisture))
            timedate = strftime("%d:%m:%Y:%H:%M:%S", localtime())
            writestring = timedate + " " + outstring
            print(writestring)
            f.write("{0},{1:0.1f}\n".format(timedate, temperature))
            f.close()
            d.write("{0},{1:0.1f}\n".format(timedate, cputemp))
            d.close()
            m.write("{0},{1:0.1f}\n".format(timedate, moisture))
            m.close()
            starttime = PLOTTING_DATA(DayMonthYear, delay)
            return(starttime)
        else:
            print('Failed to get reading. Try again!')


def PLOTTING_DATA(DayMonthYear, delay):
    xtemp = []
    ytemp = []
    xcpu = []
    ycpu = []
    xmoi = []
    ymoi = []
    print("...*GRAPHING*...")
    d = open("""/Irrigationsystem/Data/{0}/cputemp{0}.csv""".format(DayMonthYear), 'r')
    f = open("""/Irrigationsystem/Data/{0}/temperature_{0}.csv""".format(DayMonthYear), 'r')
    m = open("""/Irrigationsystem/Data/{0}/moisture_{0}.csv""".format(str(DayMonthYear)), 'r')
    tempdata = list(reader(f))
    f.close()
    for line in tempdata:
        xtemp.append(line[1])
        ytemp.append(datetime.strptime(line[0], "%d:%m:%Y:%H:%M:%S"))
    plt.style.use('dark_background')
    plt.title("Temperature Graph {0}"
    .format(strftime("%d-%m-%Y", localtime())))
    plt.xlabel("Time")
    plt.ylabel("Temperature °C")
    plt.plot(ytemp, xtemp)
    plt.gcf().autofmt_xdate()
    plt.savefig("""/Irrigationsystem/Data/{0}/data_temp_{0}.png""".format(DayMonthYear), dpi=300)
    plt.draw()
    plt.pause(delay/3)
    plt.clf()
    cpudata = list(reader(d))
    d.close()
    for line in cpudata:
        temp = float(line[1])
        xcpu.append(temp)
        ycpu.append(datetime.strptime(line[0], "%d:%m:%Y:%H:%M:%S"))
    plt.title("CPU Temp {0}".format(strftime("%d-%m-%Y", localtime())))
    plt.xlabel("Time")
    plt.ylabel("Temp °C")
    plt.plot(ycpu, xcpu)
    plt.gcf().autofmt_xdate()
    plt.savefig("""/Irrigationsystem/Data/{0}/cputemp{0}.png""".format(DayMonthYear), dpi = 300)
    plt.draw()
    plt.pause(delay/3)
    plt.clf()
    moisturedata = list(reader(m))
    m.close()
    for line in moisturedata:
        temp = float(line[1])
        xmoi.append(temp)
        ymoi.append(datetime.strptime(line[0], "%d:%m:%Y:%H:%M:%S"))
    plt.title("Moisture Graph {0}".format(strftime("%d-%m-%Y", localtime())))
    plt.xlabel("Time")
    plt.ylabel("Moisture %")
    plt.plot(ymoi, xmoi)
    plt.gcf().autofmt_xdate()
    plt.savefig("""/Irrigationsystem/Data/{0}/data_moisture_{0}.png""".format(DayMonthYear), dpi=300)
    plt.draw()
    plt.pause(delay/3)
    plt.clf()
    starttime = time.time()
    return(starttime)
