"""                                                                                                 =
relay_control.py script for managing relay states (ON/OFF) locally and remotely on Windows/Linux. It 
uses command-line arguments for control, including source directory, device identifier, remote 
credentials, relay number, and timeout duration. Supports both shorthand and full command-line 
options.

Arguments:
- State (-s, --state): Desired relay state (ON/OFF).
- Mode (-m, --mode): Operation mode (LOCAL/REMOTE).
- Source Directory (--src-dir): Relay control scripts location.
- Device (--device): Relay device identifier (e.g., COM12, /dev/ttyUSB18).
- Relay Number (-r, --relay): Relay number to control.
- Timeout (-t, --timeout): Operation timeout in seconds.
- User (--user): SSH username (default: ubuntu).
- Host (--host): SSH host (default: 192.168.1.63).

Examples:
- Local (Windows): python relay_control.py --state ON --mode LOCAL --src-dir "C:\path\to\scripts" --device COM12 --relay 0 --timeout 5
- Remote (Linux): python relay_control.py --state OFF --mode REMOTE --src-dir "/path/to/scripts" --device /dev/ttyUSB18 --relay 1 --timeout 5 --user ubuntu --host 192.168.1.63

Efficient relay management across systems and networks.
"""

import argparse
import os
import subprocess
import platform

def main():
    parser = argparse.ArgumentParser(description='Control relay on Windows and Linux, locally or remotely.')
    parser.add_argument('-s', '--state', choices=['ON', 'OFF'], required=True, help='Relay state, ON or OFF.')
    parser.add_argument('-m', '--mode', choices=['LOCAL', 'REMOTE'], required=True, help='Operation mode, LOCAL or REMOTE.')
    parser.add_argument('--src-dir', required=True, help='Source directory for relay control scripts.')
    parser.add_argument('--device', required=True, help='Device identifier, e.g., COM12 or /dev/ttyUSB18.')
    parser.add_argument('-r', '--relay', default='0', help='Relay number to use. Default is 0.')
    parser.add_argument('-t', '--timeout', default='5', help='Timeout, in seconds. Default is 5.')
    parser.add_argument('--user', default='ubuntu', help='Username for remote SSH control.')
    parser.add_argument('--host', default='192.168.1.63', help='Host for remote SSH control.')

    args = parser.parse_args()
    relay_state = '1' if args.state.upper() == 'ON' else '0'
    os_type = platform.system()

    if args.mode.upper() == 'LOCAL':
        if os_type == 'Windows':
            command = f"python {args.src_dir}\\ch340_relay_tty_control.py -d {args.device} -r {args.relay} -s {relay_state} -t {args.timeout}"
        else:  # Linux
            command = f"python3 {args.src_dir}/ch340_relay_tty_control.py -d {args.device} -r {args.relay} -s {relay_state} -t {args.timeout}"
    else:  # REMOTE
        remote_command = f"sudo chmod 0666 {args.device}; python3 {args.src_dir}/ch340_relay_tty_control.py -d {args.device} -r {args.relay} -s {relay_state} -t {args.timeout}"
        if os_type == 'Windows':
            command = f'ssh.exe {args.user}@{args.host} "{remote_command}"'
        else:  # Linux
            command = f'ssh {args.user}@{args.host} "{remote_command}"'

    # Execute command
    try:
        print(f"Executing: {command}")
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    main()
