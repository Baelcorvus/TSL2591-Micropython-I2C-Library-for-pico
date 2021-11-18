# TSL2591 Micropython I2C Library for pico
 Micropython library for the TSL2591 high precision light sensor for use on a pico microcontroller using a bus IO I2C device.

Driver for the SL2591 precision light sensor in micropython using an I2C bus device for the raspberry pi pico microcontroller
Requires the presence of the I2C_bus_device librrary from:

https://github.com/Baelcorvus/I2C_Busdevice

The repository includes a version of the I2C bus device, the driver for the sensor and a couple of examples.
First you need to copy the files `TSL2591.py` and `I2C_bus_device.py` from the repository to the default directory of you pico device.

To use call the object with the i2C bus to use and the address of the sensor.
If no address is given the default of 0x29 is used.

To use the device, first you must import the library:
 ```python
        from machine import Pin, I2C
        import TSL2591
```
then define the I2C bus the device is attached to:
```python
        sdaPIN=machine.Pin(0)
        sclPIN=machine.Pin(1)
        i2c_bus = 0
        addr = 0x29

        i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)
```    
This will define an I2C bus on pin 0 for SDA and pin 1 for SCL. The actual pins will need to be changed
to the specifics of your project. The i2c_bus will be designated by the pins used. A pinout
of your pico will call the pins sda0 and scl0 for bus 0 and sda1 and scl1 for bus 1

to define the sensor object we then use:
```python
        tsl = TSL2591.TSL2591(i2c, addr)
```        
if the address is the same as the deafult the addr can be omited (so: `tsl = TSL2591.TSL2591(i2c)`
you can now access the sensor atrributes. .lux, .infrared, .visible and .full_spectrum
so you can read the light using these attributes:
```python        
        lux = tsl.lux
        infrared = tsl.infrared
        visible = tsl.visible
        full_spectrum = tsl.full_spectrum
```

An example program is included that simply reads and prints these values (TSL_example.py) and one that shows how you 
can integrate the sensor with other I2C bus devices.

```python
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
        
    sleep(0.1)                                           #short delay - not necessary for the bus, just cosmetic, omit as needed
```
This shows how to import, define and use the properties of the sensor.

***A note on error checking.***
If an I/O error occurs during transmission the buss driver will reaise an OS Error exception. We can catch this error with `try:` and except `OSError:`
for example if we read the sensor we can do this:
```python
try:
        lux = tsl.lux
except OSError:
        lux = 0
        print("I/O error")
```

The other example is a simple program that incorportates this code into a multiple sensor situation.