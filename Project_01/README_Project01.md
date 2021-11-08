# ENGI 301 - Pokey Clicker Game! 
## Build Instructions and Operations
**By: Oscar D. Soto**



## Build Instructions - Hardware 
To begin buliding the Pokey Clicker Game, you will need the following hardware:
- PocketBeagle Development board 
- SPI Display: Adafruit 2.8" and 3.2" Color TFT Touchscreen Breakout v2
- Arcade Button: Arcade Button with LED - 30mm Translucent Red 
- 5V Piezo Buzzer: Piezo Buzzer - PS1240 
- 4-Digit 7-Segment Display w/I2C Backpack: Adafruit 0.56" 4-Digit 7-Segment Display w/I2C Backpack - Red 
- 1k Ohm Resistors: x4 
- Wires
- Male/Male jumper wires: Premium Male/Male Jumper Wires - 40 x 6" (150mm)

### PocketBeagle Setup
Setting up the PocketBeagle requires soldering




**Exercise caution when soldering, make sure to:**
- Solder in a well-ventilated room
- Not breathe in the fumes of the solder
- Always be aware of where your end of your hot iron is
- Always turn off the iron when not in use

1) Solder Long Leads with 100 mil female headers onto the outside rows of the PocketBeagle. Make sure the headers are vertically placed
2) Create a solder bridge between the USB host pins (ID to GND) and (VB to VI) in the P1 header
3) Solder Short Leads with  100 mil female headers headers onto the inside rows of the PocketBeagle. Make sure these headers are vertically placed
4) After completing these soldering connections, plug your PocketBeagle into a solderless breadboard such that the micro USB port sticks off the board



*Wiring*
To power on the PocketBeagle, connect a micro USB to the micro USB port on the PocketBeagle  

### SPI Display Setup
Setting up the SPI Display requires soldering. Be sure to utilize the same precautions as in the step above.



*Soldering* 
1) Female Long Leads with female headers onto the SPI side of the the display
2) Create a solder bridge between the IM1, IM2, and IM3 ports on the SPI side of the display


*Wiring*


Using Male/Male jumper wires, make the following connections from (SPI to PocketBeagle): 
   1) GND to P1_16 (GND)
   2) VIN to P1_14 (3.3 V)
   3) CLK to P1_8 (CLK)
   4) MISO to P1_10 (MISO)
   5) MOSI to P1_12 (MOSI)
   6) CS to P1_6 (GPIO5)
   7) D/C to P1_4 (GPIO89)
   8) PST to P1_2 (GPIO87)



### Arcade Button Setup
Setting up the Arcade Button requires soldering. Be sure to utilize the same precautions as in the steps above.

*Soldering*
1) Strip a 




