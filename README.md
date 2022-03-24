# USB ch340 Relay Switching Control
Python USB ch340 relay control
Modified from: https://github.com/Brasme/usb_ch340_4x_relay_control/blob/main/ch340_relay_control.py  
Bent Gramdal, Feb. 2021  

This script is intended to do the following:  
  
Connect to specified USB CH340 COM Port and modify its relay using a file.  The file will switch the relay state on a timer in seconds supplied in the file the script will loop through the file until EOF.  
  
TODO:  Add parser so we can input all variables on the commandline  
TODO:  Add OS detection and integrate Linux functionality  
  
