# USB ch340 Relay Switching Control
Python USB ch340 relay control.  
Modified from: https://github.com/Brasme/usb_ch340_4x_relay_control/blob/main/ch340_relay_control.py  
Bent Gramdal, Feb. 2021  

Tested on: Debian GNU/Linux 11  
This script is intended to do the following:  
Control relay from terminal adhoc style or via an input file.  The input file method can control whichever relay specified along with a time period to remain opened or closed. Example relay 1 ON for 2 seconds = 1,2  
TODO: Test on Windows 10  
    
The pyserial library is required! --> https://pyserial.readthedocs.io/en/latest/pyserial.html#installation.  Remove serial and add pyserial:  python3 -m pip uninstall serial && python3 -m pip install pyserial
