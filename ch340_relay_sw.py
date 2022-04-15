################################################################################
#Modified from: https://github.com/Brasme/usb_ch340_4x_relay_control/blob/main/ch340_relay_control.py
# Bent Gramdal, Feb. 2021
#
#READ THE COMMENTS BEFORE RUNNING
#Run:	    python3 -m ch340_relay_sw --file ch340_seed_file.txt --port COM25  --b 9600  
#File:      ch340_relay_sw.py
#Date:      2022MAR24
#Author:    William Blair
#Contact:   williamblair333@gmail.com
#Tested on: Windows 10 21H1 
#
#This script is intended to do the following:
#
#-connect to specified USB CH340 COM Port and modify its relay using a file 
#-the file will switch the relay state on a timer in seconds supplied in the file
#-the script will loop through the file until EOF
#-TODO:  Add parser so we can input all variables on the commandline
################################################################################

import threading
import serial
import time
#################################################################################

parser = argparse.ArgumentParser(description='USB ch340 Relay Control with Seed')

parser.add_argument('-f', '--file', type=str, help='Input file goes here' + \
'file,\t Required', required=True)

parser.add_argument('-p', '--port', type=str, help='Serial Port Identifier ' + \
'Use full port name, eg.. COM25 or /dev/ttyUSB0,\t Required', required=True)

parser.add_argument('-b', '--baud', type=str, help='Serial Port Baud Rate ' + \
'Confirm before inputting,\t Required', required=True)

args = parser.parse_args()

file_name   = (args.file)
port        = (args.port)
baud        = (args.baud)

seed_file   = open(file_name, 'r')
seed        = seed_file.readlines()
serial_port = serial.Serial(port, baud)

onOffStr=['Off','On']
serial_delay = 0.5
#################################################################################

def read_from_port(serial_port):
        connected=1
        while connected==1:
           try:
               chars = serial_port.readline()
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

thread = threading.Thread(target=read_from_port, args=(serial_port,))
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
    serial_port.write(statMsg)
    # Wait until thread has received status
    time.sleep(serial_delay)
    print('--------------------------------')
#################################################################################

print('--------------------------------')
print('USB Serial CH340 - Relay control')
time.sleep(serial_delay)
check_status()
#################################################################################

# We need to add some delay. The CH340 only can handle one command at a time
for delay in seed:
    serial_port.write(offMsg[0])
    time.sleep(serial_delay)
    state[0]=0

    serial_port.write(onMsg[0])
    time.sleep(serial_delay)
    state[0]=1

    print(float(delay) + "seconds delay")
    time.sleep(float(delay))
    line.delete_line(filename, 0)
    print("loop")
#################################################################################

print('Exit..')
serial_port.close()
file_name.close()
#################################################################################