OptoBLE Software Package
Jay Yang Lab, UW-Madison Dept. of Anesthesiology

Author: Ian Baumgart
		ibaumgart@wisc.edu

___________________________________________________________________________
DESCRIPTION

The OptoBLE is a fully implantable, wirelessly controlled LED neural
interface for optogenetic applications. This release accommodates two LED
channels intended for two different wavelengths of LEDs at the interface.
This system designed for use with the SwiChR channelrhodopsin 
(K. Deisseroth, Science 2014), but can be adapted for other optically
excitable channels.

The controller unit transmits simulation parameters to the implant via
Bluetooth low energy (BLE), recently renamed Bluetooth Smart. Controller
uses a simple python script, and the implant code is written in Arduino.
The controller code should be robust enough to operate on any BLE-
capable linux device, but has been tested with the Raspberry Pi 3 Model
B+. The implant code is specific to the RFduino bluetooth module
(RFD22301).

The system transmits parameters for:
	LED1ON: Stimulation time for the first LED (Implant GPIO 0)
	LED1OFF: Delay between offset of LED1 and onset of LED2 stimulation
	LED2ON: Stimulation time for the second LED (Implant GPIO 1)
	LED2OFF: Delay between offset of LED2 and onset of LED1 stimulation
	NUMCYC: Number of times to repeat the stimulation pattern

Build instructions for the controller unit and implant can be found in the
"build-instructions" document.
___________________________________________________________________________
INSTALLATION

Controller:
Install BluePy plugin and ensure the TkInter package is installed in
python. BluePy can be installed from "https://github.com/IanHarvey/bluepy"
Upload the python script "optoble.py" to your Raspberry Pi board and 
execute with root or sudo privileges.

Implant: Download the Arduino IDE and install the RFduino library. The
library can be found attached in this package and also at 
"https://github.com/RFduino/RFduino". Follow build instructions to use
the usb uploader. N.B. The board type must be set to RFduino to upload
successfully.