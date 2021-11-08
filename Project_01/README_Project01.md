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
- Wear eye protection

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
1) Strip an electrical wire at both ends
2) Loop one end through a hole underneath the arcade button to provide a strong mechanical connections. 
3) Solder this connection to provide a good electrical connection
4) Connect the other end of the stripped wire to one end of a Male/Male jumper cable by wrapping the wire around the pin.
5) Solder this connection for electrical security
6) Repeat steps 1-5 for the remaining three holes underneath the arcade button 


*Wiring*
 
 
 Using Male/Male jumper cables, make the following connections 
   1) Ground the two cables on either side of the ("-") symbol underneath the button. *It is recommended to ground these with the GND from the PocketBeagle located on P2_21. For optimal results, use a separate half-breadboard for the button connection, with the (-) rail grounded to this pin on the PocketBeagle.* 
   2) Attach the cable from the ("+") side of the symbol underneath the button to a 3.3V power connection on the PocketBeagle. *It is recommended to supply 3.3V from P2_23 on the positive power rail of the half-breadboard recommended in step 1.*
   3) Attach the last remaining jumper cable such that it shares a row with a 1 kOhm pullup resistor (A pullup resistor should be connected from the positive rail on the half breadboard to the row it is sharing with the jumper cable) and a connection leading from a GPIO connection on the PocketBeagle to the same row. *For the same results, use GPIO59 (P2_2)* 

### 4 Digit, 7-Segment Display Setup 
This particular 7-segment display uses an I2C backpack to take advantage of the PocketBeagle's I2C connection capacilities. Connect this display to another half-sized solderless breadboard (separate from the half-sized solderless breadboard used for the button circuit) and make the following connections: 


*Wiring*
1) Attach one end of a Male/Male jumper cable to pin P2_9 (SCL) on the PocketBeagle. Attach the other end of the jumper cable to the "C" connection fromn the I2C backpack. 
2) Attach one end of a Male/Male jumper cable to pin P2_11 (SDA) on the PocketBeagle. Attach the other end of the jumper cable to the "D" connection from the I2C backpack. 


**NOTE: connections 1 and 2 require 1 kOhm pullup resistors as described in the Arcade Button  Setup *Wiring* Section. Please consult for how to wire a pullup resistor** 

3)  Supply a 3.3V voltage supply to the "+" connection on the I2C backpack
4)  Ground the "-" connection on the I2C backpack

**NOTE: for steps 3 and 4, it is recommended to supply 3.3V to the positive power rail of the breadboard, and to GND the negative rail using the same pins from the PocketBeagle as in the arcade button wiring


### Piezo Buzzer Setup


*Wiring*
1) Ground the negative end of the Piezo speaker
2) Using a Male/Male Jumper cable, connect one of the PWM pins to the positive end of the Piezo speaker 




