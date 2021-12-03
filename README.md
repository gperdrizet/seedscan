# seedscan
Simple python utility using scanimage and ffmpeg to make long duration timelapse videos with a flatbed scanner.

## Setup notes
### Scanner permissions
By default USB scanner can only be accessed by scanimage via sudo. To allow user acces, find the scanner's vendor and product hex IDs with **lsusb**. IDs are the two colon seperated values after 'ID'.
```
$ lsusb
$ Bus 001 Device 002: ID 04b8:0110 Seiko Epson Corp. GT-8200U/GT-8200UF [Perfection 1650/1650 PHOTO]`
```
Then add the following to a file named **50-usb-epsonscanner.rules** (or something similar) in **/etc/udev/rules.d** using your vendor and product IDs.
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTR{idProduct}=="0110", MODE="0666"
```
Reboot and you should be able to use scanimage without sudo.

### Cron
Scanns are triggered via a cron job. Add the following to the user's cronfile (i.e. **crontab -e**). A scan every 10 minutes seems like a good place to start, but this can be changed to fit the experiment.
```
*/10 * * * * python /path/to/seedscan/scan.py
```

### CircuitPython (for sensors)
To run the temp/humidity/pressure sensors, we need CircuitPython and the library for the sensor (AdaFruit MS8607)First. I am using a RasperryPi Zero W for which detailed instructions can be found here: [CircuitPython](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi), [MS8607 library](https://learn.adafruit.com/adafruit-te-ms8607-pht-sensor/python-circuitpython). Here is the short version.

Check that you are running python 3* and pip to match, then install CircuitPython:
```
$ sudo pip3 install --upgrade setuptools
$ sudo pip3 install --upgrade adafruit-python-shell
$ wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
$ sudo python3 raspi-blinka.py
```
Note: this will set python 3 as system wide default and requires a reboot to complete. Also, output indicates that pre-installing setuptools may be unnecessary.

Then install the library for the MS8607:
```
sudo pip3 install adafruit-circuitpython-ms8607
``` 
Last thing is to change permissions so that non-root users can access I2C devices:
```
$ sudo groupadd i2c
$ sudo chown :i2c /dev/i2c-1
$ sudo chmod g+rw /dev/i2c-1
$ sudo usermod -aG i2c user
```
Then you should be able to access ic2-i withou t elevating privileges. Test is with:
```
i2cdetect -y 1
```
