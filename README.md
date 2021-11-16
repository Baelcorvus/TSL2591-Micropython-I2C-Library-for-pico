# TSL2591 Micropython I2C Library for pico
 Micropython library for the TSL2591 high precision light sensor for use on a pico microcontroller using a bus IO I2C device.
 
 
 

    to use call the object with the i2C bus to use and the address of the sensor.
    If no address is given the default of 0x29 is used.

    To use the device, first you must import the library:
 ```python
        from machine import Pin, I2C
        from I2C_bus_device import I2CDevice
        import TSL2591
```
    then define the I2C bus the device is attached to:

        sdaPIN=machine.Pin(0)
        sclPIN=machine.Pin(1)
        i2c_bus = 0
        addr = 0x29

        i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)
    
    Will define an I2C bus on pin 0 for SDA and pin 1 for SCL. The actual pins will need to be changed
    to the specifics of your project. The i2c_bus will be designated by the pins used. A pinout
    of your pico will call the pins sda0 and scl0 for bus 0 and sda1 and scl1 for bus 1
    
    to define the sensor object we then use:

        tsl = TSL2591.TSL2591(i2c, addr)
        
    if the address is the same as the deafult the addr can be omited (so: tsl = TSL2591.TSL2591(i2c)
    you can now access the sensor atrributes. .lux, .infrared, .visible and .full_spectrum
    so you can read the light using these attributes:
        
        lux = tsl.lux
        infrared = tsl.infrared
        visible = tsl.visible
        full_spectrum = tsl.full_spectrum