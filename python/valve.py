# Creator: Graham Driver
# Desc: It just sends a High signal to a relay that opens a solenoid valve.
import RPi.GPIO as gpio

def SETUP(valve):
    gpio.setmode(gpio.BCM)
    gpio.setup(valve, gpio.OUT)


def OPEN(valve):
    SETUP(valve)
    gpio.output(valve, 0)
    print("Open!")

def CLOSE(valve):
    SETUP(valve)
    gpio.output(valve, 1)
    print("Closed!")
