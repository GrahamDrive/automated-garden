# Creator: Graham Driver
# Desc: This script is used to pull weather data from "openweathermap.org" via
# an API grab. It then checks the likelyhood of heavy rain and in turn returns
# a value of True or False along with printing the data to console.
import requests
import xml.etree.ElementTree as ET
import time as t


def REPORT():
    #This Api grabs an XML containing a 5 day 3 hour forecast
    try:
        resp = requests.get("""https://api.openweathermap.org/data/2.5/forecast?id=524901&q=Winnipeg,ca&mode=xml&appid=25d2568bc66f3ecad087fe15220a3990""")
    except:
        return(False)
    else:
        tree = ET.fromstring(resp.content)
        try:
            forecast = tree[4]
        except:
            return(False)
        else:
            time = forecast[0]
            date = time.attrib
            #The local time will be used later
            #to verfiy how long is left in the current forecast.
            timetest = t.localtime()
            hour = timetest[3]
            #The XML is organised into 3 hour trees for 5 days
            #so I simply grab the next 3 hour window
            endforecast = date["to"]
            startforecast = date["from"]
            #Given Time in XML is UTC format this it is converted to CDT
            #will need to be adjust for daylight savings but due to
            #main usage in summer months not needed
            starthour = int(startforecast[11:13]) - 5
            endhour = int(endforecast[11:13]) - 5
            startminute = startforecast[14:16]
            endminute = endforecast[14:16]
            if starthour <= 0 and starthour < 5:
                starthour = starthour + 24
            if endhour <= 0 and endhour < 5:
                endhour = endhour + 24
            precipitation = time[1].attrib
            temp = time[4].attrib
            realMin = timetest[4]
            if realMin < 10:
                realMin = str(realMin)
                realMin = "0{0}".format(realMin)
            #The data is now output to the console and a
            #True or False value is returned wehter
            #it is likely to rain in the next 3 hours.
            print("")
            print("*WEATHER REPORT*")
            print("Recieved at {0}:{1}".format(hour, realMin))
            tempC = float(temp["value"])-273.15
            print("Temp: {0:.2f}°C".format(tempC))
            if 'value' in precipitation:
                print("Rain between {0}:{1} and {2}:{3}"
                        .format(starthour, startminute, endhour, endminute))
                rainMm = float(precipitation['value'])
                print("{0}mm".format(rainMm))
                print("")
                if rainMm >= 0.8:
                    return(True)
                else:
                    return(False)
            else:
                print("No Rain between {0}:{1} and {2}:{3}"
                    .format(starthour, startminute, endhour, endminute))
                print("")
                return(False)
