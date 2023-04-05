from machine import ADC, Pin, Timer, I2C
from array import array
import utime

phRead = ADC(2)
pHtimer = Timer()

#corrects to voltage on adc pin
factorADC = 3.3 / (65535)

def read(pHtimer):
    print(phRead.read_u16() * factorADC)


pHtimer.init(freq= 20, mode=Timer.PERIODIC, callback=read)  