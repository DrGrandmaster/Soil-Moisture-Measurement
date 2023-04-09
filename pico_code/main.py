from machine import ADC, Pin, Timer, I2C
from array import array
import utime

phRead = ADC(2)
pHtime = Timer()

moistRead = ADC(1)
moistTime = Timer()

tempRead = ADC(4)
tempTime = Timer()

#corrects to voltage on adc pin
factorADC = 3.3 / (65535)

#corrects to numerical readings
factorPH = 1.0
factorMoist = 1.0

def readPH(pHtimer):
    print(phRead.read_u16() * factorADC * factorPH)

def readMoist(moistTime):
    print(moistRead.read_u16() * factorADC * factorMoist)

def readTemp(tempTime):
    print(27 - ((tempRead.read_u16() * factorADC) - 0.706)/0.001721)


pHtime.init(freq= 20, mode=Timer.PERIODIC, callback=readPH) 
moistTime.init(freq= 20, mode=Timer.PERIODIC, callback=readMoist)
tempTime.init(freq= 20, mode=Timer.PERIODIC, callback=readTemp)