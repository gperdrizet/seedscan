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
import config
import os.path
from PIL import Image

# First check to see what scan we are on - if we don't have
# a scan number logged, assume it is the first scan and set
# scan number to one. 

if os.path.exists(config.SCAN_COUNT):

    # Read scan count from file
    with open(config.SCAN_COUNT, 'r') as f:
        scan_count = int(f.read())

        # Incrament the scan count
        scan_count += 1
else:

    # Scan count file does not exist - set scan count to 1
    scan_count = 1

    # Since this is the first scan of the run, make the output
    # directory to hold the scans
    os.mkdir(config.SCAN_DIR)

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