"""
====================================================================================================
Relay Control Script (relay_control.py)

Description:
This script provides functionality for controlling relay modules via a serial interface. It supports 
ad-hoc command line control and automated control via an input file. The script can toggle individual 
relays on or off for specified durations.

Usage Examples:
- Command line (Linux): python3 relay_control.py -d '/dev/ttyUSB0' -r 1 -t 5
- Command line (Windows): python relay_control.py -d COM1 -b 9600 -r 1 -t 1
- With input file: python relay_control.py -f playfile.txt

Arguments:
- -d (--device): Serial device (e.g., '/dev/ttyUSB0' or 'COM1').
- -b (--baud): Baud rate for serial communication. Default is 9600.
- -r (--relay): Relay number to control.
- -t (--timeout): Duration in seconds to keep the relay in the set state.
- -f (--file): Input file for automated relay control.

File Format (for automated control):
Each line in the input file should contain two comma-separated values:
1. Relay number
2. Duration in seconds
Example: '1,2' turns relay 1 on for 2 seconds.

Author: William Blair
Contact: williamblair333@gmail.com
Date: 2022SEP29
Original Source: Modified from Brasme's implementation (Feb. 2021)
Source URL: https://github.com/Brasme/usb_ch340_4x_relay_control/blob/main/ch340_relay_control.py

Tested On:
- Debian GNU/Linux 11+
- Windows 10+

Notes:
- Requires pyserial package. Remove serial if installed. 
- python3 -m pip uninstall serial && python3 -m pip install pyserial
- https://pyserial.readthedocs.io/en/latest/pyserial.html#installation.  Remove serial and add pyserial:  
- Ensure proper permissions for serial port access on Windows / Linux systems.

TODO:

Disclaimer:
This script is provided "as is", without warranty of any kind. Use at your own risk.
====================================================================================================
"""

import argparse
import csv
import datetime
import logging
import serial
import threading
import time

class RelayController:
    def __init__(self, port, baud=9600):
        self.serial_port = serial.Serial(port, baud)
        self.state = [0] * 8
        self.on_msgs = [bytes([160, i+1, 1, 161+i]) for i in range(4)]
        self.off_msgs = [bytes([160, i+1, 0, 160+i]) for i in range(4)]
        self.stat_msg = b'\xFF'
        self.thread = threading.Thread(target=self.read_from_port)
        self.thread.start()

    def read_from_port(self):
        while True:
            try:
                chars = self.serial_port.readline()
                a = chars.split()
                if len(a) == 2:
                    n = {b'CH1:':0, b'CH2:':1, b'CH3:':2, b'CH4:':3,
                         b'CH5:':4, b'CH6:':5, b'CH7:':6, b'CH8:':7}.get(a[0],0)
                    onOff = {b'OFF':0, b'ON':1}.get(a[1],0)
                    if n >= 0:
                        print(f"Relay: {n} = {'Off' if onOff == 0 else 'On'}")
                        self.state[n-1] = onOff
                elif len(chars) > 0:
                    print(f"Relay: {chars.decode()}")
            except:
                print("Relay: Terminated")
                break

    def relay_status(self):
        print("--------------------------------------------------")
        print('Checking status')
        self.serial_port.write(self.stat_msg)
        time.sleep(0.5)
        print("--------------------------------------------------")

    def relay_on_off(self, relay_number, on=True, time_out=1):
        msg = self.on_msgs[relay_number] if on else self.off_msgs[relay_number]
        print(f"Setting relay {relay_number} to {'ON' if on else 'OFF'} for {time_out} seconds.")
        self.serial_port.write(msg)
        self.state[relay_number] = 1 if on else 0
        time.sleep(time_out)

    def log_relay_operation(self):
        cycle_time_start = datetime.datetime.now()
        logging.info("Cycle finish")
        cycle_time_finish = datetime.datetime.now()
        logging.info(f"Cycle time total {cycle_time_finish - cycle_time_start}")

    def execute_from_file(self, file_name):
        with open(file_name) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                relay_num = int(row[0])
                timeout = int(row[1])
                self.relay_on_off(relay_num, time_out=timeout)
        self.log_relay_operation()

    def close(self):
        self.serial_port.close()

def setup_logging():
    logging.basicConfig(filename='relay.log', encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def parse_args():
    parser = argparse.ArgumentParser(description='Relay Control Script')
    parser.add_argument('-d', '--device', required=True, help='Device /dev/ttyUSB or COM port.')
    parser.add_argument('-b', '--baud', default=9600, help='Set device baud rate. Default is 9600.')
    parser.add_argument('-r', '--relay', type=int, default=0, help='Relay number to use. Default is 0.')
    parser.add_argument('-s', '--set', type=int, choices=[0, 1], help='Change relay state. Set to 0 for OFF or 1 for ON.')
    parser.add_argument('-t', '--timeout', type=int, default=1, help='Timeout in seconds. Default is 1.')
    parser.add_argument('-f', '--file', help='Relay seed/play file for automated relay input.')
    parser.add_argument('-i', '--info', action='store_true', help='Get information regarding device and exit.')
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging()

    controller = RelayController(args.device, args.baud)

    if args.info:
        controller.relay_status()
        print("Operation complete.")
        controller.close()
        return

    if args.set is not None:
        controller.relay_on_off
