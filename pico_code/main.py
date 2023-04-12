import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
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

# Wifi Transfer
ssid = 'Design_Wifi'
password = 'Water123'
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

###
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

###
def webpage(temperature):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)
###
def serve(connection):
    #Start a web server
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        temperature = pico_temp_sensor.temp
        html = webpage(temperature)
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
