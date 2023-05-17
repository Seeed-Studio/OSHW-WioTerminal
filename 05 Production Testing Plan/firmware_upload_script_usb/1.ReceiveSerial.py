import serial
from serial.tools import list_ports
from time import sleep



def find_device():
    while True:
        port = None
        for p in list_ports.comports():
#            print p[2]
            if p[2].upper().startswith('USB VID:PID=2886:802D'):
                port = p[0]
                print('find Wio terminal port: ' + port)
                return port

        sleep(0.1)

        
Wio_port=find_device()
WioSerial = serial.Serial(port=Wio_port,baudrate=115200,bytesize=8,stopbits=1,timeout=1)
while True:
    line = WioSerial.readline().strip()
    if line !="":
        print line
    if "RTL8720 Wireless PASS" in line:
        break


