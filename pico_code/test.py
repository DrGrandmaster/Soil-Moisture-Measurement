from machine import Pin, I2C

readI2C = I2C(0x36, scl=Pin(15), sda=Pin(14), freq=115200)

readI2C.start()

