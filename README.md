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
*/10 * * * * python3.7 /home/siderealyear/arkk/seedscan/scan.py
```
