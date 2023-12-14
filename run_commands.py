"""
====================================================================================================
Command Runner Script (run_commands.py)

Description:
This script is designed to automate the execution of a series of commands listed in a specified file. 
It can execute the commands a specified number of times or continuously in an infinite loop. This 
script is particularly useful for repetitive tasks, such as testing or automation sequences.

Usage:
1. Finite number of cycles: python run_commands.py commands.txt 10
2. Infinite execution: python run_commands.py commands.txt infinite

Arguments:
- file: The filename containing the list of commands to be executed. Each command should be on a 
  separate line.
- cycles: The number of times the command list should be executed. Specify an integer for finite 
  execution or 'infinite' for continuous execution.

Example File Format:
Each line in 'commands.txt' should contain a single command to be executed.
Example:
    python relay_control.py -d COM3 -b 115200 -r 1 -s 1 -t 30
    python relay_control.py -d COM3 -b 115200 -r 1 -s 0 -t 10

Notes:
- Ensure that the commands in the file are compatible with the operating system and environment where 
  the script is run.
- The script uses Python's subprocess module for command execution, which should be used with caution 
  to avoid security risks, especially when executing commands from untrusted sources.

Author: William Blair
Contact: williamblair333@gmail.com
Date: 2023DEC13

Disclaimer:
This script is provided "as is", without warranty of any kind. Use at your own risk. The author is 
not responsible for any damage or loss resulting from the use of this script.
====================================================================================================
"""

import argparse
import subprocess

def run_commands_from_file(file_name):
    """
    Reads and executes commands from the given file.
    """
    with open(file_name, 'r') as file:
        commands = [line.strip() for line in file.readlines()]
    return commands

def parse_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Run Commands from File Script')
    parser.add_argument('file', help='File containing the list of commands to execute')
    parser.add_argument('cycles', nargs='?', default='infinite', 
                        help="Number of cycles (1-65536) or 'infinite'")
    return parser.parse_args()

def main():
    args = parse_arguments()

    try:
        cycles = float('inf') if args.cycles == 'infinite' else int(args.cycles)
    except ValueError:
        print("Error: Cycles must be a number or 'infinite'")
        return

    if not (1 <= cycles <= 65536) and cycles != float('inf'):
        print("Error: Cycles must be between 1 and 65536")
        return

    commands = run_commands_from_file(args.file)
    count = 0
    while count < cycles:
        for command in commands:
            subprocess.run(command, shell=True)
        count += 1

if __name__ == "__main__":
    main()
