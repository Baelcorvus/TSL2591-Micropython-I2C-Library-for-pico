'''
Example of an integrated sensor system with multiple I2C devices on the same bus.
This example uses a potential of up to 4 sensors, a TSL2591 high precision light sensor
a SI7021 temperatur and humidity sensor, a SHTC3 temperature and humidity sensor and
a slave arduino microcontroller simply receiving the status of a button and reporting
the state of a button connected to it.
'''

'''first we import the libraries for the devics - if you do not have the libraries for unused
sensors put a # infront of a library
'''
from machine import Pin, I2C
from time import sleep
import TSL2591
import SI7021
import Ard_obj
import shtc3

'''
Then we define the I2C as it is physically connected to out pico
'''
sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
i2c_bus = 0

i2c=machine.I2C(i2c_bus, sda=sdaPIN, scl=sclPIN, freq=400000)

'set up the addresses of the sensors'
ard_addr = 0x09
lux_addr = 0x29
temp_addr = 0x40
sht_addr = 0x70

'tell the example program which devices are attached to the bus'
ard_attached = True
tsl_attached = True
si_attached = True
sht_attached = False

'''
now we create and intialise the objects.
ard will now always talk to the arduino slave, and similarly
tsl will always communicate with the tsl2591 light sensor,
si will always communicate with the si7021 sensor and
sht will always talk to the shtc3 sensor
'''
if (ard_attached): ard = Ard_obj.ard_obj(i2c, ard_addr)
if (tsl_attached): tsl = TSL2591.TSL2591(i2c, lux_addr)
if (si_attached):
    si = SI7021.Si7021(i2c, temp_addr)
    print(si.identifier)
if (sht_attached):
    sht = shtc3.SHTC3(i2c, sht_addr)
    print(sht._chip_id)

'here we define an external LED (on pin 28) and a button (on pin 20) so we can communicate their states to the arduino.'
led = machine.Pin(28, Pin.OUT)
led.low()

but2 = Pin(20, Pin.IN, Pin.PULL_UP)


while True:    
    if (ard_attached):       #if we have the arduino attached and it has been found send the button state and receive the arduino button state
        if (ard.device.i2c_error == 0):
            button = ard.read_write(but2.value())
            if (button == 1):
                led.high()
            else:
                led.low()
        else:                #this will be triggered if the arduino is supposed to be on the bus, but no adrino is found'
            print("no ardino")
            print(ard.device.i2c_error, hex(ard.device.i2c_error_device))
            ard = Ard_obj.ard_obj(i2c, ard_addr)    #reinitialise the object to look again'
 
    if(tsl_attached):        #if a TSL2591 light sensor is attached and had been found read the lux value
        if(tsl.device.i2c_error == 0):
            lux = tsl.lux
            print("lux: {}  ".format(lux), end = '')
        else:                #if the TSL2591 is attached but not been found, report this and look again.
            lux = 0
            print("no lux")
            print(tsl.device.i2c_error,hex( tsl.device.i2c_error_device))
            tsl = TSL2591.TSL2591(i2c, lux_addr)
    if(si_attached):
        if(si.device.i2c_error == 0):  #if an si7021 temperature and humidity sensor is present read both values.
            temperature, humidity = si.measurments 
            print("temperature: {}  Relative_humidity {}  ".format(temperature, humidity), end = '')
        else:                          #if no SI7021 detected then complain and reinitialise the sensor.
            temperature = 0 
            humidity = 0
            print("no temp")    
            print(si.device.i2c_error, hex(si.device.i2c_error_device))
            si = SI7021.Si7021(i2c, temp_addr)
    if(sht_attached):                  #if a SHTC3 temperature and humidity sensor is present read both values.     
        if(sht.device.i2c_error == 0):
            temperature2, humidity2 = sht.measurements
            print("temperature: {}  Relative_humidity {}  ".format(temperature2, humidity2), end = '')
        else:                         #if no SHTC3 detected then complain and reinitialise the sensor.
            temperature2 = 0
            humidity2 = 0
            print("no temp2")
            print(sht.device.i2c_error, hex(sht.device.i2c_error_device))
            sht = shtc3.SHTC3(i2c, sht_addr)
    print("")
    sleep(0.1)     #give the bus a rest before reading again. You can omit this for maximum data throughput.
    
    