"""
Run all core module servers.
"""

import os
import sys

if sys.version_info[0] != 3 or sys.version_info[1] < 5:
    print('Python 3.5 or above is required.')
    sys.exit(1)


def main():
    """Main entry point."""
    from . import run_modules

    print('┌────────────────────────────────────────────────┐')
    print('│  PEACOCK: A Virtual Stock Market Simulator     │')
    print('└────────────────────────────────────────────────┘')

    if len(os.sys.argv) != 2:
        print("Missing configuration filename.")
        print("USE: python3 -m peacock config_file.xml")
        exit(0)

    filename = os.sys.argv[1]
    if not filename.endswith('.xml'):
        filename += '.xml'

    # Save PID in file
    pid_fn = 'peacock_' + filename[:-4].replace('/', '_') + '.pid'
    with open(pid_fn, 'w') as pid_file:
        pid_file.write(str(os.getpid()) + '\n')

    run_modules(filename)


main()
