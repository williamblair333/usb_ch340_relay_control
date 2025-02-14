# Relay Control and Command Runner Scripts
<img src="CH340_relay_race.png" alt="CH340 Relay Race" style="width:50%;">


This repository contains two Python scripts for controlling relay modules and automating command execution. The `relay_control.py` script is used for controlling relays via a serial interface, while `run_commands.py` automates the execution of a series of commands from a file.

## Contents

1. [relay_control.py](#relay_controlpy)
2. [run_commands.py](#run_commandspy)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Disclaimer](#disclaimer)
6. [Author](#author)

## relay_control.py

This script provides functionality for controlling relay modules via a serial interface. It supports ad-hoc command-line control and automated control via an input file.

### Features

- Control individual relays on/off for specified durations
- Read relay control sequences from an input file for automation
- Command line based, easy to integrate with other systems

### Requirements

- Python 3
- pyserial package

### Usage Examples

- Command line (Linux):

````sh
python3 relay_control.py -d '/dev/ttyUSB0' -r 1 -t 5
````

- Command line (Windows):

````sh
python relay_control.py -d COM1 -b 9600 -r 1 -t 1
````

- With input file:

````sh
python relay_control.py -f playfile.txt
````

## run_commands.py

A script to automate the execution of a series of commands listed in a specified file. It can execute the commands a specified number of times or continuously in an infinite loop.

### Features

- Execute commands from a file
- Supports finite or infinite execution cycles
- Useful for repetitive tasks and automation

### Usage Examples

- Finite number of cycles:

````sh
python run_commands.py commands.txt 10
````

- Infinite execution:

````sh
python run_commands.py commands.txt infinite
````

## Installation

### Do This First
Save yourself a lot of headache. Let's use `/dev/ttyUSB0` as the reference CH340 device:

````sh
# Disconnect USB device if connected
sudo systemctl mask brltty-udev.service
sudo apt-get remove --yes brltty
# Reconnect USB device if disconnected
sudo chmod 0666 /dev/ttyUSB0
````

We test everything in Ubuntu (currently 22.04). For Windows, you’d probably need to run as Administrator.

### Download The Source
To use these scripts, clone this repository or download the scripts directly. Ensure Python 3 is installed on your system.

````sh
git clone https://github.com/your-repository/relay-automation.git
cd relay-automation
pip uninstall serial
pip install pyserial
````

## Usage

### relay_control.py

Run the script with the required arguments. For example:

````sh
python relay_control.py -d COM1 -b 9600 -r 1 -t 1
````

### run_commands.py

Create a file (e.g., `commands.txt`) with each command on a new line and run the script:

````sh
python run_commands.py commands.txt 10
````

For infinite execution:

````sh
python run_commands.py commands.txt infinite
````

## Disclaimer

These scripts are provided "as is", without warranty of any kind. Use at your own risk. The author is not responsible for any damage or loss resulting from the use of these scripts.

## Author

````
Name: William Blair  
Contact: Create an Issue
`
