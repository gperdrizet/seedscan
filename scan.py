'''SeedScan: simple python utility to make long duration timelapse
videos of germinating seeds in a flatbed scanner.
Copyright (C) 2021  George A. Perdrizet II

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

import subprocess
import os.path
import argparse
import board
import busio
from PIL import Image
from datetime import datetime
from adafruit_ms8607 import MS8607

import config

# Instantiate command line argument parser
parser = argparse.ArgumentParser(description='Controls scanner and sesnors.')

# Add argument to specify whether or not to read sensor data
parser.add_argument('--sensors', dest='sensors', action='store_true')
parser.add_argument('--no-sensors', dest='sensors', action='store_false')
parser.set_defaults(sensors=False)

# Add argument to specify whether or not to scan
parser.add_argument('--scan', dest='scan', action='store_true')
parser.add_argument('--no-scan', dest='scan', action='store_false')
parser.set_defaults(scan=True)

# Parse the args
args = parser.parse_args()
print(f'Sensors arg reads {args.sensors}')

# First check to see what scan we are on - if we don't have
# a scan number logged, assume it is the first scan and set
# scan number to one. 

if os.path.exists(config.SCAN_COUNT) == True:

    # Read scan count from file
    with open(config.SCAN_COUNT, 'r') as f:
        scan_count = int(f.read())

        # Incrament the scan count
        scan_count += 1
else:

    # Scan count file does not exist - set scan count to 1
    scan_count = 1

    # Since this is the first scan of the run, we may need to 
    # make the output directory to hold the scans - if the 
    # directory exist, it's OK, continute. Means that someone 
    # probably deleted the scan count file by hand

    if os.path.exists(config.SCAN_DIR) == False:
        os.mkdir(config.SCAN_DIR)

    # Also, if we are running the sensors, create the sensor data 
    # file and write the header

    if args.sensors == True:
        with open(config.SENSOR_DATA, 'w') as f:
            f.write(f'scan_number,datetime,pressure_hPa,temp_C,rel_humidity\n')


# If we are running the sensors, collect the data
print(f'Done with pre-prep, checking sensors: {args.sensors}')

if args.sensors == True:
    # Before doing the scan, read sensor data - the scan takes about
    # 2 minutes with my scanner and I worry that the light might raise
    # the temperature. Doing the sensor read just before the scan will
    # give a better idea about the conditions in the scanner over the
    # previous 10 minutes since the last scan.

    # Read sensors
    print(f'Reading sensors')
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = MS8607(i2c)

    # Get current time
    scantime = datetime.now()

    # Write sensor data to file
    with open(config.SENSOR_DATA, 'a') as f:
        f.write(f'{scan_count},{scantime},{sensor.pressure},{sensor.temperature},{sensor.relative_humidity}\n')

# If we want to acquire a scan
print(f'Acquiring scan: {args.scan}')

if args.scan == True:

    # Set up zero padded file name for new scan
    file_name = f'{scan_count:04}.{config.SCAN_FORMAT}'
    output = f'{config.SCAN_DIR}/{file_name}'

    # Construct scan command using parameters from config.py
    scan_command = " ".join([
        'scanimage',
        f'--format={config.SCAN_FORMAT}',
        f'--resolution={config.RESOLUTION}',
        f'--mode={config.SCAN_MODE}',
        f'>{output}'
    ])

    # Do the scan
    os.system(scan_command)

    # Rotate image 90 degrees to landscape if desired
    if config.LANDSCAPE == True:
        img = Image.open(output)
        img = img.rotate(-90, expand=1)
        img.save(output)

# Write the updated scan count
with open(config.SCAN_COUNT, 'w') as f:
    f.write(f'{scan_count}')
