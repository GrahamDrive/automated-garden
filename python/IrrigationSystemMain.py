# Creator: Graham Driver
# Desc: This is the Main script of the custom irrigation system it first sets
# up the 2.4Ghz transceiver to work as a master with an arduino sensor slave.
# After recieveing the packet of data it is used to determine soil moisture
# air temp based on that info along with a 3 hour forecast it is determined
# a Solenoid valve is opened to water the garden.
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import Temperature
import valve
import weatherForecast as weather
from cpuTemp import getCPUtemperature
import sys
#import Email

GPIO.setmode(GPIO.BCM)
Dry = 410
Water = 288
Wet = 327
# *NOTE* Most of the nrf24 coding is not Graham Drivers Creation but
# a sample code used Source: https://www.youtube.com/watch?v=_68f-yp63ds
# Radio Setup Starts Here

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()
# radio.startListening()
interval = int(input("How long often would you like to check in minutes? "))
interval = interval * 60
message = list("GETDATA")
while len(message) < 32:
    message.append(0)
starttime = time.time()
while(1):
    if float(getCPUtemperature()) > 70:
        #Email.SENDMAIL("""Irrigation System
        #                overheat and shutdown""", "Overheat!")
        sys.exit("OverHeating")
    start = time.time()
    radio.write(message)
    print("")
    print("Sent the message: {}".format(message))
    radio.startListening()

    while not radio.available(0):
        time.sleep(1 / 100)
        break

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))

    print("Translating the received Message into unicode characters")
    string = ""
    for n in receivedMessage:
        # Decode into standard unicode set
        if (n >= 32 and n <= 126):
            string += chr(n)
    dataarray = string.split()
    print("Out received message decodes to: {}".format(dataarray))
    if dataarray:
        end = time.time()
        difference = end - starttime
        print(difference)
        if difference >= interval:
            delay = 1
        elif difference < interval and difference >= 0:
            delay = interval - difference
        elif difference < 0:
            delay = 0
        print("delay is {}s".format(delay))
        try:
            moistureNumber = float(dataarray[1])
        except:
            print("Error In Received Packets")
        else:
            # At this point the previously calibrated moisture level
            # is tested and with the weather report result it will
            # determine wether to water or not.
            if moistureNumber > Dry and weather.REPORT() is False:
                valve.OPEN(16)
                time.sleep(60)
                valve.CLOSED(16)
            elif moistureNumber < 327:
                time.sleep(5)
                valve.CLOSE(16)
            elif moistureNumber <= Water:
                valve.CLOSE(16)
            moisturePercentage = ((moistureNumber - Water)/Dry)
            starttime = Temperature.MAIN(dataarray[0], delay, moisturePercentage, getCPUtemperature())
        radio.stopListening()
        time.sleep(1)
