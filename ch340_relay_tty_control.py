#---------------------------------------------------------------------------------
#READ THE COMMENTS BEFORE RUNNING
#Modified from: https://github.com/Brasme/usb_ch340_4x_relay_control/blob/main/ch340_relay_control.py
#Bent Gramdal, Feb. 2021
#Run:	    python3 -m ch340_relay_tty_control -s '/dev/ttyUSB10' -r 1 -t 5 -f playfile.txt
#File:      ch340_relay_tty_control.py
#Date:      2022SEP29
#Author:    William Blair
#Contact:   william.blair@enersys.com
#Tested on: Debian GNU/Linux 11
#This script is intended to do the following:
#-Control relay from terminal adhoc style or via an input file.  The input file 
#-method can control whichever relay specified along with a time period to remain
#-opened or closed. Example relay 1 ON for 2 seconds = 1,2
#TODO: Test on Windows 10
#NOTE: You MUST uninstall serial and install pyserial package (pip install py..
#---------------------------------------------------------------------------------

import argparse, csv, datetime, logging, serial, threading, time

parser = argparse.ArgumentParser(description='Setup ')

parser.add_argument('-d', '--device', type=str, help='Device /dev/ttyUSB or COM' + \
' port. Required', required=True)
parser.add_argument('-b', '--baud', type=str, help='Set device baud rate.' + \
' Default is 9600. Optional', required=False)
parser.add_argument('-r', '--relay', type=int, help='Relay number ' + \
'to use. Default is 0. Optional', required=False)
parser.add_argument('-s', '--set', type=int, help='Change relay state. ' + \
'to use. Set to 0 for OFF or 1 for ON. Optional', required=False)
parser.add_argument('-t', '--timeout', type=int, help='timeout, in seconds. zero ' + \
'may or may not work.  Default is 1. Optional', required=False)
parser.add_argument('-f', '--file', type=str, help='Relay seed\play file. Use to ' + \
'granularly control and automate relay input. No default, Optional', required=False)
parser.add_argument('-i', '--info', help='Get information regarding device ' + \
'and exit. Optional',  action='store_true', required=False)

args             = parser.parse_args()
tty_port         = (args.device)
serial_baud      = (args.baud)
serial_port      = serial.Serial(tty_port, 9600)
relay_number     = (args.relay)
relay_state_set  = (args.set)
time_out         = (args.timeout)
file_name        = (args.file)
relay_info       = (args.info)

logging.basicConfig(filename='relay.log', encoding='utf-8', level=logging.DEBUG, \
    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#---------------------------------------------------------------------------------

#Relay logic goes here
state = [0,0,0,0]
onOffStr=['Off','On']
onMsg  = [ b'\xA0\x01\x01\xA2', b'\xA0\x02\x01\xA3', b'\xA0\x03\x01\xA4', b'\xA0\x04\x01\xA5' ]
offMsg = [ b'\xA0\x01\x00\xA1', b'\xA0\x02\x00\xA2', b'\xA0\x03\x00\xA3', b'\xA0\x04\x00\xA4' ]
statMsg = b'\xFF'
#---------------------------------------------------------------------------------

def read_from_port(serial_port):
    connected=1
    while connected==1:
       try:
           chars = serial_port.readline()
           a=chars.split()
           if len(a) == 2:
               n={b'CH1:':0,b'CH2:':1,b'CH3:':2,b'CH4:':3, b'CH5:':4, b'CH6:':5, b'CH7:':6, b'CH8:':7}.get(a[0],0)
               onOff={b'OFF':0,b'ON':1}.get(a[1],0)
               if n >= 0:
                   print("Relay:",n,"=",onOffStr[onOff])
                   state[n-1]=onOff
           elif len(chars) > 0:
               print("Relay:",chars)
       except:
           print("Relay: Terminated")
           connected=0
#---------------------------------------------------------------------------------

def relay_status():
    print("--------------------------------------------------")
    print('Checking status')
    serial_port.write(statMsg)
    #Wait until thread has received status
    time.sleep(0.5)
    print("--------------------------------------------------")
#---------------------------------------------------------------------------------

#Serial_port.write(onMsg[0]) for 1st relay, [1] for 2nd relay, etc..
#State[0][1] equal closed and [0][0] = open 
#We need to add some delay. The CH340 only can handle one command at a time
#---------------------------------------------------------------------------------

def relay_msg(relay_number):
    print("Setting relay", end=" ")
    print(relay_number, end=" ")
#---------------------------------------------------------------------------------
    
def relay_off(serial_port, relay_number, state, time_out):
    relay_msg(relay_number)
    print("to OFF / Open position", end=" ")
    print("for", time_out, end=" ")
    print("seconds.")
    serial_port.write(offMsg[relay_number])
    state[0]=0
    time.sleep(time_out)       
#---------------------------------------------------------------------------------

def relay_on(serial_port, relay_number, state, time_out):
    relay_msg(relay_number)
    print("to ON / Closed position")
    print("for", time_out, end=" ")
    print("seconds.")
    serial_port.write(onMsg[relay_number])
    state[0]=1
    time.sleep(time_out)    
#---------------------------------------------------------------------------------

def relay_logging():
    cycle_time_start = datetime.datetime.now()
    logging.info("Cycle finish")
    cycle_time_finish = datetime.datetime.now()
    cycle_time_total = cycle_time_finish - cycle_time_start
    logging.info("Cycle time total {}".format(cycle_time_total))
#---------------------------------------------------------------------------------

def relay_file_read(file_name):
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            temp_relay = int(row[0])
            temp_time_out = int(row[1])
            print("Manipulating circuit on relay #", temp_relay, end=" ")
            print("for", temp_time_out, end=" ")
            print("seconds.")            
            relay_off(serial_port, temp_relay, state, 1)
            relay_on(serial_port, temp_relay, state, temp_time_out)
    csvfile.close()
    relay_off(serial_port, temp_relay, state, 1)
#---------------------------------------------------------------------------------

#Set optional variables if not defined
if serial_baud:
    serial_port   = serial.Serial(tty_port, serial_baud)

#Start querying the relay device here
thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()

if relay_info:
    relay_status()
    print("Operation complete.")
    serial_port.close()
    exit()

if not relay_number:
    relay_number = 0

if relay_state_set == 0:
    relay_off(serial_port, relay_number, state, time_out)
   
elif relay_state_set == 1:
    relay_on(serial_port, relay_number, state, time_out)
    
if not time_out:
    time_out = 1

if file_name:
    relay_file_read(file_name)
    relay_logging() 
#---------------------------------------------------------------------------------

print("Operation complete.")
serial_port.close()
#---------------------------------------------------------------------------------