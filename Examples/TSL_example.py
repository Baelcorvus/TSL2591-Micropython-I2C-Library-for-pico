'''
Code to use a TSL2591 high precision light sensor with a pico microcontroller
in micropython using a I2C bus device.
'''

'''first we import the libraries'''
from machine import Pin, I2C
from time import sleep
import TSL2591

'''Then we define the physical I2C that the sensor is connected to''' 
sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
i2c_bus = 0

i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)

lux_addr = 0x29

'''and finnaly set up the sensor object that will always talk to the sensor'''
try:
    tsl = TSL2591.TSL2591(i2c, lux_addr)
    chip_id = tsl._chip_id
    if (chip_id== 0x50):
        identifier = "TSL2591"
    else:
        identifier = "other sensor"
except OSError:
    print ("TSL2591 not present")
else:
    print('{} is present'.format(identifier))

while True:
    try:
        lux = tsl.lux                                              #read the lux value
        infrared = tsl.infrared                                    #read the infrared value
        visible = tsl.visible                                      #read the visible value
        full_spectrum = tsl.full_spectrum                          #read the full_spectrum value
                                                                   #the most useful value for many projects is the lux value.
        print("Lux: {}  ".format(lux), end = '')                   
        print("Infrared: {}  ".format(infrared), end = '')
        print("Visible: {}  ".format(visible), end = '')
        print("Full Spectrum: {}  ".format(full_spectrum), end = '\r')
    except OSError:
        print("TSL2591 I/O Error - retrying connection")

    sleep(0.1)                                           #read every half second - not necessary ofr the bus, just cosmetic, omit as needed
