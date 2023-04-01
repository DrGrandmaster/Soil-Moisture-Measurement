from machine import ADC, Pin, Timer

phRead = ADC(2)
pHtimer = Timer()

def read(pHtimer):
    print(phRead.read_u16())

pHtimer.init(freq= 1, mode=Timer.PERIODIC, callback=read)