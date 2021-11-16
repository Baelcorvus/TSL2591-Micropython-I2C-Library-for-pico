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
tsl = TSL2591.TSL2591(i2c, lux_addr)

while True:
    if(tsl.device.i2c_error == 0):
        lux = tsl.lux                                              #read the lux value
        infrared = tsl.infrared                                    #read the infrared value
        visible = tsl.visible                                      #read the visible value
        full_spectrum = tsl.full_spectrum                          #read the full_spectrum value
                                                                   #the most useful value for many projects is the lux value.
    else:                                                   #simple error checking. If no device is found the porperty tsl.device.i2c_error will be not zero.
        lux = 0                                             #if it is not zero, complain and attempt to reinitialise the object, settling the values to zero.
        infrared = 0
        visible = 0
        full_spectrum = 0        
        print("no lux")
        print(tsl.device.i2c_error,hex( tsl.device.i2c_error_device))
        tsl = TSL2591.TSL2591(i2c, lux_addr)

    print("Lux: {}  ".format(lux), end = '')                   
    print("Infrared: {}  ".format(infrared), end = '')
    print("Visible: {}  ".format(visible), end = '')
    print("Full Spectrum: {}  ".format(full_spectrum))
    sleep(0.5)                                           #read every half second - not necessary for the bus, just cosmetic, omit as needed