# Relay Control and Command Runner Scripts

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

- Command line (Linux): `python3 relay_control.py -d '/dev/ttyUSB0' -r 1 -t 5`
- Command line (Windows): `python relay_control.py -d COM1 -b 9600 -r 1 -t 1`
- With input file: `python relay_control.py -f playfile.txt`

## run_commands.py

A script to automate the execution of a series of commands listed in a specified file. It can execute the commands a specified number of times or continuously in an infinite loop.

### Features

- Execute commands from a file
- Supports finite or infinite execution cycles
- Useful for repetitive tasks and automation

### Usage Examples

- Finite number of cycles: `python run_commands.py commands.txt 10`
- Infinite execution: `python run_commands.py commands.txt infinite`

## Installation

To use these scripts, clone this repository or download the scripts directly. Ensure Python 3 is installed on your system.

git clone https://github.com/your-repository/relay-automation.git
cd relay-automation

Install the required Python package:

pip install pyserial

## Usage
relay_control.py

Run the script with the required arguments. For example:

python relay_control.py -d COM1 -b 9600 -r 1 -t 1

run_commands.py

Create a file (e.g., commands.txt) with each command on a new line and run the script:

python run_commands.py commands.txt 10

For infinite execution:

python run_commands.py commands.txt infinite

## Disclaimer

These scripts are provided "as is", without warranty of any kind. Use at your own risk. The author is not responsible for any damage or loss resulting from the use of these scripts.

## Author

    Name: William Blair
    Contact: Create an Issue

This README provides a complete and comprehensive guide for both the `relay_control.py` and `run_commands.py` scripts, including their features, usage examples, installation instructions, and disclaimer. Please replace `[Your Name]`, `[Your Email]`, and the repository URL with your actual details.

