# Connect FLDIGI on the Macbook Pro with Big Sur (11.5.2) to Yaesu FT-991 (non-A)

## Load CP210x VCP Drivers 
If you have not already done so, or did with a version prior to 6.0.1, follow these steps 
1. Disconnect everything from the MacBook except LAN/WiFi
1. Reboot.
1. Download **CP210x VCP Mac OSX Driver** from [Silicon Labs Download page](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
1. Unzip the `Mac_OSX_VCP_Driver.zip` file
1. Launch the `SiLabsUSBDriverDisk.dmg` file by double clicking on it from **Finder**
    1. If you have a previous version of the driver, 
        1. Double click the uninstaller.sh and follow the prompts.
        1. Reboot, and follow the next step.
    1. Double click the `Install CP210x VCP Driver.app` file
        1. Follow the Prompts
1. Reboot.

## Configure the Radio
To Configure the Radio, you can change the Menu items as follows. In the Menu, default values appear as blue.
|Menu Item #|Menu Item Name|Item Value Range|Default Value|Prefered Value|
|----------:|:-------------|----------------|-------------|:------------:|
|31|CAT RATE|4800/9600/19200/38400 bps|4800 bps|**38400 bps**|
|32|CAT TOT|10/100/1000/3000 msec|10 msec|10 msec|
|33|CAT RTS|ENABLE/DISABLE|ENABLE|ENABLE|
|46|AM OUT LEVEL|0-100|50|**100**|
|59|CW FREQ DISPLAY|DIRECT FREQ/PITCH OFFSE|PITCH OFFSE|PITCH OFFSE|
|60|PC KEYING|OFF/DAKY/RTS/DTR|OFF|**DTR**|
|62|DATA MODE|PSK/OTHERS|PSK|**OTHERS**|
|63|PSK TONE|1000/1500/2000 Hz|1000 Hz|**1500 Hz**|
|64|OTHER DISP (SSB)|-3000 - 0 - 3000 10Hz Step|0 Hz|**1500 Hz**|
|65|OTHER SHIFT (SSB)|-3000 - 0 - 3000 10Hz Step|0 Hz|**1500 Hz**|
|66|DATA LCUT FREQ|OFF/100-1000 (50Hz Step)|300 Hz|300 Hz|
|67|DATA LCUT SLOPE|6 dB/oct / 18 dB/oct|18 dB/oct|18 dB/oct|
|68|DATA HCUT FREQ|700-4000 (50Hz Step)|3000 Hz|**3600 Hz**|
|69|DATA HCUT SLOPE|6 dB/oct / 18 dB/oct|18 dB/oct|18 dB/oct|
|70|DATA IN SELECT|REAR/MIC|REAR|REAR|
|71|DATA PTT SELECT|DAKY/RTS/DTR|DAKY|DAKY|
|72|DATA PORT SELECT|DATA/USB|DATA|**USB**|
|73|DATA OUT LEVEL|0-100|50|**100**|
|74|FM MIC SELECT (PHONE)|MIC/REAR|MIC|MIC|
|75|FM OUT LEVEL|0-100|50|50|
|76|FM PKT PTT SELECT|DAKY/RTS/DTR|DAKY|**DTR**|
|77|FM PKT PORT SELECT|DATA/USB|DATA|DATA|
|106|SSB MIC SELECT|MIC/REAR|MIC|MIC|
|107|SSB OUT LEVEL|0-100|50|50|
|108|SSB PTT SELECT|DAKY/RTS/DTR|DAKY|DAKY|
|109|SSB PORT SELECT|DATA/USB|DATA|**USB**|
|110|SSB TX BPF|100-3000/100-2900/200-2800/300-2700/400-2600|300-2700|300-2700|
|114|IF NOTCH WIDTH|NARROW/WIDE|WIDE|**NARROW**|
|141|TUNER SELECT|OFF/INTERNAL/EXTERNAL/ATAS/LAMP|INTERNAL|**ATAS**|
|146|DATA VOX GAIN|0-100|50|50|
|147|DATA VOX DELAY	100|30-3000 msec|100 msec|100 msec|
|148|ANTI DVOX GAIN|0-100|0|0|
||||||


## Connect the Radio
Use the [RT-42 USB-A to USB-B 6-Ft Cable](https://www.rtsystemsinc.com/RT-42-USB-A-to-USB-B-6-Ft-Cable_p_542.html) cable from RT Systems




## Using the FT-991A with fldigi and flrig

CAT control involves both software and settings on the radio itself. The default radio settings on the FT-991A are not likely to work “out of the box”.

Some initial things to verify are in place:

1. Download and install the USB driver for the radio. NOTE: be sure the USB cable is UNPLUGGED from the
computer when you install the driver regardless of the OS your are using.
- If you’re using Windows get the driver from Icom or use the one on the CD that comes with the radio.
- If using Linux or MacOS then get the drivers direct from [Silcon Labs]([https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers). Note: Some versions of Linux have a driver
built in.

Note: For MacOS High Sierra and later be sure to go to Security & Privacy in the System Configuration
settings and in the General tab allow the driver to be accessed. Without doing that it will be unusable.

2. Download the latest version of Fldigi. I also highly recommend downloading flrig
for transceiver control. Flrig is written as a companion to fldigi and adds much greater rig control than is possible with just fldigi. It is especially good with the FT991A. I basically only touch the radio to turn it on or off when running digital modes, and even that can be automated.

Download both from [W1HKJ web site](www.w1hkj.com).

It is highly recommend that you also download the flrig and fidigi help pdf files from the  [W1HKJ web site](www.w1hkj.com)  website. They are well written help files. Fldigi's help is hundreds of pages long and has a great deal of helpful info. When you get to installing fldigi it will be a big help to you and should guide you in the setting of the necessary and optional parameters. Once it’s running there are so many features to use that are not always obvious that reading it or at least a detailed scan through it should be a goal.

### FT-991A settings

On the rig, press the MENU button.  Then change these menu items as shown:

Menu # | Name | Value
---------- | ---------- | ------ 
31	 | CAT RATE	 | 38400 bps
32	 | CAT TOT	 | 10 msec
33	 | CAT RTS	 | ENABLE
59	 | CW FREQ DISPLAY	 | PITCH OFFSET
60	 | PC KEYING	 | DTR
62	 | DATA MODE	 | OTHERS
63	 | PSK TONE	 | 1500 hZ
64	 | OTHER DISP (SSB)	 | 1500 Hz
65	 | OTHER SHIFT (SSB)	 | 1500 Hz
66	 | DATA LCUT FREQ	 | 300 Hz
67	 | DATA LCUT SLOPE	 | 18 dB/oct
68	 | DATA HCUT FREQ	 | 3600 Hz
69	 | DATA HCUT SLOPE	 | 18 dB/oct
70	 | DATA IN SELECT	 | REAR
71	 | DATA PTT SELECT	 | DAKY
72	 | DATA PORT SELECT	 | USB
73	 | DATA OUT LEVEL (RX)	 | 100
74	 | FM MIC SELECT (PHONE)	 | MIC
75	 | FM OUT LEVEL (Rx)	 | 50
76	 | FM PKT PTT SELECT	 | DTR
77	 | FM PKT PORT SELECT	 | DATA
106	 | SSB MIC SELECT	 | MIC
107	 | SSB OUT LEVEL	 | 50
108	 | SSB PTT SELECT	 | DAKY
109	 | SSB PORT SELECT	 | USB
110	 | SSB TX BPF	 | 300-2700
114	 | IF NOTCH WIDTH	 | NARROW
146	 | DATA VOX GAIN	 | 50
147	 | DATA VOX DELAY	 | 100 msec
148	 | ANTI DVOX GAIN	 | 0

### Software setup
You should have already installed the driver for the built-in sound card in the FT-991A.

Connect the rig to the computer with a USB A-Male to B-Male cable and turn on the radio.

Install fldigi and flrig.  On Windows the programs install to their own folders and should be installed in the normal application directory where other apps are installed. Putting them in other folders can causes permissions issues sometimes on Windows 10. For Mac and Linux install them as you would any other application.For those choosing to use flrig continue below, otherwise scroll down to the RigCat setup:

### flrig control option
First, we get flrig going then it’s easy to configure fldigi to use flrig for xcvr control.

With the radio on and the USB cable connected and no other communications program running, Start flrig.  It will come up with just a basic display. 

![alt-text][flrig.console]
![alt-text][TSL2591]

Go to the menu

Config/Setup/Transceiver.
<center>
[[alt-text][flrig.config.xcvr]]
</center>
Choose the FT991A from the Rig dropdown list. That will select the default settings which will work on . Note: The RTS +12v and DTR +12v boxes do not normally need to be checked.

#### Now choose the Serial Port to use
###### Mac / Linux
Select the SilconLabs driver from the dropdown list. If it isn't in the list then click the SerPort button to repopulate the list. It if still isn't in the list then the driver is not loading for some reason like the radio is not on or connected or the driver has not been installed properly so that needs to be rectified before going on. If you're using MacOS High Sierra or a later version of MacOS you may need to authorize the driver install in Security & Privacy setup in System Preferences after runing the install program. There will be a message on the General page if it has been blocked.
###### Windows 
Open the device manager and determine to which com port the serial driver from Silcon Labs is assigned and choose that from the drop down list. Verify that the Baud rate in flrig matches the baud rate selected in the rig. It's better to choose a fixed baud rate than Auto.  Now, click the Init button. It should go from red to black lettering. If it does not go to black lettering then verify all of the above again, especially baud rate and echo.

Next select the restore tab
<center>
[![alt text][flrig.config.restore]]
</center>
and choose whether you want flrig to save and restore all the radio’s parameters on startup and exit or whether you want it to open with the same settings as the rig is currently using.  If Use xcvr data is checked flrig will start up with the same settings as the rig currently is using.

Select the poll tab
<center>
[[img src=flrig.ft991a.poll.png]]
</center>
and click the Set All buttons for the initial polling options. You can play with these values later if you wish. The larger the number the slower the response time to button pushes etc, but also the less load on the system so there is a balance. A very fast machine can use all ones, but there is normally no need to add the additional load to your system for that.

Flrig now should have control of the rig so changing frequency in flrig will changed the frequency on the rig and visa versa. The buttons and sliders should do as they are labeled.

I would recommend before you move on that you go to the Config/UI menu and select Tooltips. They are a great help to the new user to figure out what each control does as not all are labeled.  You can choose 4 different UI’s from the narrow one with small sliders (I use this one – see above screen shot of flrig), to a narrow one with large sliders, to a wide version or a touch version.  Now close flrig and restart it to be sure all is well . Everything should be working and you should be able to change frequency on the radio and flrig should follow.

Configure fldigi for use with flrig/FT991A.

Start fldigi and fill in the initial setup pages presented. You can ignore the last page for now. All these pages can be accessed via the configuration menu later to be changed as you wish.  Since you've chosen to use flrig then go to the fldigi menu “Configuration/Rig control/flrig” and check the top box to tell fldigi to use flrig for rig control with fldigi as client.   Leave the other controls at their default setting.
<center>
[[img src=ft991a-fldigi-flrig.png]]
</center>
Once that is done fldigi should communicate with flrig and changes such as frequency or bandwidth in flrig or fldigi should be reflected in the other. If the lower box is checked then flrig will send fldigi audio to the radio when the PTT button is clicked otherwise PTT will just key the rig with no power out. Click Save at the bottom of the page.

Setup DATA-U as the mode and bandwidth as 3000 for now.
<center>
[[img src=ft991a-fldigi-mode-bw.png]]
</center>
All that is left is to customize fldigi for how you want to operate. Many things can be changed such as the UI scheme, colors, Macros, and many more. Read the help manual to learn about all the options and features that are available.
> [flrig manual as pdf file](http://www.w1hkj.com/files/flrig/flrig-help.pdf)
> [on-line html manual](http://www.w1hkj.com/flrig-help/)

### RigCat rig control option
To setup RigCat you first must download the IC7100.xml file and save it to the “Rigs” directory of the fldigi directory .

[FT991A xml file](http://www.w1hkj.com/files/xmls/yaesu/FT-991A.xml)

###### Mac/Linux
Put the file in $HOME/.fldigi/rigs/
###### Windows
Open the file finder.  Find the fldigi.files directory and put it in the rigs directory. Where the fldigi.files directory is different depending on the version of Windows. It is normally under the user's name.  Once the IC7100.xml file is in place then start fldigi. It will run you through the basic setup pages.  Ignore the last setup page for now.

Start fldigi and after it is up and running
<center>
[[img src=ft991a-fldigi-rigcat.png]]
</center>
with the basic setup then from the menu choose from the menu Configuration/Rig control/RigCat. At the upper left “Rig description” click Open and choose the IC7100.xml file already downloaded. Once the rig description file is selected then verify that the Baud Rate is the same as the radio.

Choose the Device from the drop down list. On Mac or Linux there should be a device for the SilLab USBtoUart. On Windows check the device manager in Windows to see which Com port is assigned to the USB-Uart device on the radio. and then choose that Com port.

Verify that the only check boxes checked are Commands are Echoed, CAT command for PTT, and Restore Settings on close.

Check the box at the top to “Use RigCat” and then click Initialize. The lettering should go from red to black. At this point you should have rig control from fldigi and changing frequencies in fldigi should be reflected on the radio and visa versa. Set the bandwidth desired and mode to DATA-U for digital mode use in fldigi.
<center>
[[img src=ft991a-fldigi-mode-bw.png ]]
</center>
### Final Setup

With fldigi running verify you have a blue waterfall running. If you don't see that then there is a problem with the audio input to fldigi. Verify the Soundcard setup.

Note:
  * For MacOS Mojave and later you must enable the microphone for fldigi in Security & Privacy in the System Preferences settings.
  * For Windows 10 be sure to grant permission for fldigi to access the Microphone.


Now we will verify the power out of the radio. Set the radio power control on the rig to max, 100%
and leave it there.

Set Power Meter scale:
  * Flrig: Right click on the lower portion of the S-meter scale and choose the power scale desired.  
  * RigCat: Menu – Configuration>UI>Clrs/Fnts>FreqDisp/Meters. Choose power scale and Save.

Note: The max digital power out used for a QSO should cause no ALC action on the radio. The FT991A will put out quite a bit of power without ALC action, but you don't want to interfere with other close signals on the band either so ideally the power should be between 25-40 watts.

Fldigi has a Transmit Attenuator at the lower right of the fldigi window and this is used to make small adjustments in power. I set mine at 9 then adjust the radio's menu item, USB MOD Level to get 30 watts of power. This allows you to add more power or reduce power as needed in fldigi with the Transmit Attenuator without touching the radio. Note: Higher numbers in the attenuator mean lower output.

Note: In Windows there is the Windows Mixer that is also in the audio stream so that will need to be included in the audio level adjustments in and out for the radio's built-in sound card.

Now click on the Tune button in fldigi upper right corner. That should put the rig into transmit. The actual power output will be dependent on the audio drive to the radio. Adjust the audio stream as described above to get about 30 watts of power with the transmit attenuator set to what ever you choose for a default number. Fldigi defaults to 3.

You should now have working copies of flrig and fldigi and be ready for a digital QSO.

Checkout the default macros. Feel free to customize them and also setup a few macros for those personal information things you always want to send like, Name, Signal report, QTH, Grid Loc, your station configuration etc. It's your software and station so set it up as you wish. Remember to read the manuals. You'll learn how to make so much better use of this fantastic software and radio.

The waterfall appearance may be adjusted by the numbers at the bottom left under the waterfall.  Default settings are 0 and 60. You may want to raise the 60 to 70 to increase the contrast. Feel free to adjust the numbers for the look you like best.

Now that you’re up and running, there are two things that need to be done to get the best decoding:

  - Adjust the receive audio level. Fldigi-help.pdf, Paragraph 2.9, pg 20
  - Calibrate the sound card. Fldigi-help.pdf, Paragraph 6.3, pg 295



<style type="text/css">
   /* Indent Formatting */
   /* Format: 1-A-I-1-a-i */
   ol {list-style-type: decimal;}
   ol ol { list-style-type: upper-alpha;}
   ol ol ol { list-style-type: upper-roman;}
   ol ol ol ol { list-style-type: decimal;}
   ol ol ol ol ol { list-style-type: lower-alpha;}
   ol ol ol ol ol ol { list-style-type: lower-roman;}
   /* https://www.w3schools.com/cssref/pr_list-style-type.asp */
   /* https://stackoverflow.com/questions/11445453/css-set-li-indent */
   /* https://stackoverflow.com/questions/13366820/how-do-you-make-lettered-lists-using-markdown */
</style> 

[FT991DU]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/FT991DU.jpeg "FT-991 in Data-USB mode"
[fldigi.config.soundcard.devices]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/fldigi.config.soundcard.devices.png "fldigi Config/Sound Card values""
[fldigi.config.operator-station]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/fldigi.configure.operatior-station.png "fldigi Config/Operation-Station values"
[fldigi.config.rig-control.flrig]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/fldigi.configure.rig-control.flrig.png "fldigi Config/rig-controll flrig"
[fldigi.config.rig-control.flrig2]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/fldigi.configure.rig-control.flrig2.png "fldigi Config/rig-controll flrig2"
[fldigi.console.no-waterfall]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/fldigi.console.no-waterfall.png "fldigi Console with no waterfall working"
[fldigi.console.vfo]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/fldigi.console.vfo.png "fldigi Console (vfo portion)" 
[fldigi.console]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/fldigi.png "fldigi Console"
[flrig.config.pool]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/flrig.configure.poll.png "flrig Config/poll options - this may be a bug"
[flrig.config.ptt-generic]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/flrig.configure.ptt-generic.png "flrig Config/PTT-Generic options"
[flrig.config.restore]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/flrig.configure.restore.png "flrig Config/restore options"
[flrig.config.tcpip]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/flrig.configure.tcpip.png "flrig Config/tcpip options"
[flrig.config.xcvr]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/flrig.configure.xcvr.png "flrig Config/xcvr options"
[flrig.console]: https://github.com/DonBower/HamGoBox/blob/master/fldigi/images/flrig.png "Unconfigured Console"

[TSL2591]: https://github.com/DonBower/HamGoBox/blob/master/Images/TSL2591.jpg "High Dynamic Range Digital Light Sensor"
