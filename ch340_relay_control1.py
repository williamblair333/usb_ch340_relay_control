#Modified from: https://github.com/Brasme/usb_ch340_4x_relay_control/blob/main/ch340_relay_control.py
# Bent Gramdal, Feb. 2021

import threading
import serial
import time
import line
#################################################################################
filename = 'ch340_seed_linear_hundredth_360.txt'
#filename = 'ch340_seed_linear_ten_second.txt'
seed_file = open(filename, 'r+')
seed = seed_file.readlines()
seed_file.close()

serialPort = serial.Serial('COM25', 9600)
state = [0,0,0,0]
onOffStr=['Off','On']
#################################################################################

def read_from_port(serialPort):
        connected=1
        while connected==1:
           try:
               chars = serialPort.readline()
               a=chars.split()
               if len(a) == 2:
                   n={b'CH1:':1,b'CH2:':2,b'CH3:':3,b'CH4:':4}.get(a[0],0)
                   onOff={b'OFF':0,b'ON':1}.get(a[1],0)
                   if n > 0:
                       print('Relay:',n,'=',onOffStr[onOff])
                       state[n-1]=onOff
               elif len(chars) > 0:
                   print('Relay:',chars)
           except:
               print('Relay: Terminated')
               connected=0
#################################################################################

thread = threading.Thread(target=read_from_port, args=(serialPort,))
thread.start()
#################################################################################

# The CH340 accepts a binary coded message to turn on/off or query the status
onMsg  = [ b'\xA0\x01\x01\xA2', b'\xA0\x02\x01\xA3', b'\xA0\x03\x01\xA4', b'\xA0\x04\x01\xA5' ]
offMsg = [ b'\xA0\x01\x00\xA1', b'\xA0\x02\x00\xA2', b'\xA0\x03\x00\xA3', b'\xA0\x04\x00\xA4' ]
statMsg = b'\xFF'
#################################################################################

def check_status():
    print('--------------------------------')
    print('Checking status')
    serialPort.write(statMsg)
    # Wait until thread has received status
    time.sleep(0.5)
    print('--------------------------------')
#################################################################################

print('--------------------------------')
print('USB Serial CH340 - Relay control')
time.sleep(1)
check_status()

#################################################################################

# We need to add some delay. The CH340 only can handle one command at a time
for delay in seed:
    print("start")
    serialPort.write(offMsg[0])
    time.sleep(1)
    state[0]=0

    serialPort.write(onMsg[0])
    time.sleep(1)
    state[0]=1

    print(float(delay))
    time.sleep(float(delay))
    line.delete_line(filename, 0)
    print("loop")
    
#################################################################################

print('Exit..')
serialPort.close()
time.sleep(1)
#################################################################################