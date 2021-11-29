# seedscan
Simple python utility using scanimage and ffmpeg to make long duration timelapse videos with a flatbed scanner.

## Setup notes
### Scanner permissions
By default USB scanner can only be accessed by scanimage via sudo. To allow user acces:
1. Find vendor and product hex IDs with lsusb:
`$ lsusb`
