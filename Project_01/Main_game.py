# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Main Game Script
--------------------------------------------------------------------------
License:   
Copyright 2021 Oscar Soto

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Software API:

  SPI_DISPLAY()
    - Provide i2c bus that dispaly is on
    - Provide i2c address for the display
    
    blank()
      - Fills the display with black (i.e. color (0,0,0))
    
    fill(color)
      - Fills the display with the given (R, G, B) color tuple
    
    image(filename, rotation=90)
      - Erases display and shows image from filename
    
    text(value, fontsize=24, fontcolor=(255,255,255), backgroundcolor=(0,0,0), 
                justify=LEFT, align=TOP, rotation=90):
      - Erases display and shows text value on display
      - Value can either be a string or list of strings for multiple lines of text
      
    update_image(filename,rotaiton)
        - Coordinates with the GPIO button to update the position of the image on the 
        SPI display. The image will move from the left end of the screen to the right end.
    
    HT16K33()
        - Class to manage a HT16K33 I2C display
        
    setup()
        - Initialize the HEX Display with commands from the os library
        
    encode()
        - Encode data to TM1637 format. 
        - This function will convert the data from decimal to the TM1637 data
    
    set_digit()
        - uses the os library to set the digits on the HEX Display
        
    set_digit_raw(digit_number, data, double_point=False):
         - Update the given digit of the display using raw data value
    
    set_colon(enable):
        - Set the colon on the display.
        - Allows you to add a colon on the HEX display

    blank():
        - Clear the display to read nothing

    clear():
        - Clear the display to read '0000'

    update(value):
        - Update the value on the HEX display.
        - This function will clear the display and then set the appropriate digits
        - param value: Value must be between 0 and 9999.
        - Will throw a ValueError if number is not between 0 and 9999.
    
    text(value):
        - UpdateS the value on the display with text
        - :param value:  Value must have between 1 and 4 characters
        - Will throw a ValueError if there are not the appropriate number of 
        characters or if characters are used that are not supported.
        
    cleanup():
        # Clean up the HEX display to a message so that we know it's done
        
        
    BuzzerSound():
        - Class to manage the 5V piezo buzzer
        
    
    play_tone(frequency, length):
        - Plays a given note for a given length
    
    end():
        - Terminates the note played by play_tone
        

--------------------------------------------------------------------------
Background Information: 

Links:
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/overview
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/spi-wiring-and-test
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-wiring-and-setup
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-usage

  - https://circuitpython.readthedocs.io/projects/rgb_display/en/latest/api.html#module-adafruit_rgb_display.rgb
  - https://circuitpython.readthedocs.io/projects/rgb_display/en/latest/_modules/adafruit_rgb_display/rgb.html
  
Software Setup:
  - sudo apt-get update
  - sudo pip3 install --upgrade Pillow
  - sudo pip3 install adafruit-circuitpython-busdevice
  - sudo pip3 install adafruit-circuitpython-rgb-display
  - sudo apt-get install ttf-dejavu -y

"""

#Import the apporiate libraries used by the script

import time
import busio
import board
import digitalio

from PIL import Image, ImageDraw, ImageFont

from   adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341
import subprocess
import Adafruit_BBIO.GPIO as GPIO
import game_timer_stopwatch as GTS

import os
import sys
import math
import random
import Adafruit_BBIO.PWM as PWM


# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# HEX Display Constants 

LEFT               = 0
RIGHT              = 1
TOP                = 2
BOTTOM             = 3
CENTER             = 4

PADDING            = -5                # May need to adjust based on font

HEX_DIGITS                  = [0x3f, 0x06, 0x5b, 0x4f,     # 0, 1, 2, 3
                               0x66, 0x6d, 0x7d, 0x07,     # 4, 5, 6, 7
                               0x7f, 0x6f, 0x77, 0x7c,     # 8, 9, A, b
                               0x39, 0x5e, 0x79, 0x71]     # C, d, E, F

LETTERS                     = { "a" : 0x77, "A" : 0x77,    # "A"
                                "b" : 0x7c, "B" : 0x7c,    # "b"
                                "c" : 0x58, "C" : 0x39,    # "c", "C"
                                "d" : 0x5e, "D" : 0x5e,    # "d"
                                "e" : 0x79, "E" : 0x79,    # "E"
                                "f" : 0x71, "F" : 0x71,    # "F"
                                "g" : 0x6F, "G" : 0x6F,    # "g"
                                "h" : 0x74, "H" : 0x76,    # "h", "H"
                                "i" : 0x04, "I" : 0x30,    # "i", "I"
                                "j" : 0x0e, "J" : 0x0e,    # "J"
# Cannot be implemented         "k" : None, "K" : None,    
                                "l" : 0x38, "L" : 0x38,    # "L"
# Cannot be implemented         "m" : None, "M" : None,    
                                "n" : 0x54, "N" : 0x54,    # "n"
                                "o" : 0x5c, "O" : 0x3f,    # "o", "O"
                                "p" : 0x73, "P" : 0x73,    # "P"
                                "q" : 0x67, "Q" : 0x67,    # "q"
                                "r" : 0x50, "R" : 0x50,    # "r"
                                "s" : 0x6D, "S" : 0x6D,    # "S"
                                "t" : 0x78, "T" : 0x78,    # "t"
                                "u" : 0x1c, "U" : 0x3e,    # "u", "U"
# Cannot be implemented         "v" : None, "V" : None,    
# Cannot be implemented         "w" : None, "W" : None,    
# Cannot be implemented         "x" : None, "X" : None,    
                                "y" : 0x6e, "Y" : 0x6e,    # "y"
# Cannot be implemented         "z" : None, "Z" : None,    
                                " " : 0x00,                # " "
                                "-" : 0x40,                # "-"
                                "0" : 0x3f,                # "0"
                                "1" : 0x06,                # "1"
                                "2" : 0x5b,                # "2"
                                "3" : 0x4f,                # "3"
                                "4" : 0x66,                # "4"
                                "5" : 0x6d,                # "5"
                                "6" : 0x7d,                # "6"
                                "7" : 0x07,                # "7"
                                "8" : 0x7f,                # "8"
                                "9" : 0x6f,                # "9"
                                "?" : 0x53                 # "?"
                              }                               

CLEAR_DIGIT                 = 0x7F
POINT_VALUE                 = 0x80

DIGIT_ADDR                  = [0x00, 0x02, 0x06, 0x08]
COLON_ADDR                  = 0x04

HT16K33_BLINK_CMD           = 0x80
HT16K33_BLINK_DISPLAYON     = 0x01
HT16K33_BLINK_OFF           = 0x00
HT16K33_BLINK_2HZ           = 0x02
HT16K33_BLINK_1HZ           = 0x04
HT16K33_BLINK_HALFHZ        = 0x06

HT16K33_SYSTEM_SETUP        = 0x20
HT16K33_OSCILLATOR          = 0x01

HT16K33_BRIGHTNESS_CMD      = 0xE0
HT16K33_BRIGHTNESS_HIGHEST  = 0x0F
HT16K33_BRIGHTNESS_DARKEST  = 0x00

# No constants for the SPI display, button, or Piezo Speaker

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class SPI_Display():
    """ Class to manage an SPI display """
    reset_pin  =  None
    dc_pin     =  None
    cs_pin     =  None
    spi_bus    =  None
    display    =  None
    button     =  None
    reset_time =  None
    
    def __init__(self, clk_pin=board.SCLK, miso_pin=board.MISO, mosi_pin=board.MOSI,
                       cs_pin=board.P1_6, dc_pin=board.P1_4, reset_pin=board.P1_2,
                       baudrate=24000000, rotation=90, button="P2_2", reset_time = 3.0):
        """ SPI Display Constructor
        
        
        :param clk_pin   : Value must be a pin from adafruit board library
        :param miso_pin  : Value must be a pin from adafruit board library
        :param mosi_pin  : Value must be a pin from adafruit board library
        :param cs_pin    : Value must be a pin from adafruit board library
        :param dc_pin    : Value must be a pin from adafruit board library
        :param reset_pin : Value must be a pin from adafruit board library
        :param baudrate  : SPI communication rate; default 24MHz
        :param rotation  : Rotation of display; default 90 degrees (landscape)
        
        """
        # Configuration for CS and DC pins:
        self.reset_pin = digitalio.DigitalInOut(reset_pin)
        self.dc_pin    = digitalio.DigitalInOut(dc_pin)
        self.cs_pin    = digitalio.DigitalInOut(cs_pin)

        # Setup SPI bus using hardware SPI
        self.spi_bus   = busio.SPI(clock=clk_pin, MISO=miso_pin, MOSI=mosi_pin)

        # Create the ILI9341 display:
        self.display    = ili9341.ILI9341(self.spi_bus, cs=self.cs_pin, dc=self.dc_pin,
                                         baudrate=baudrate, rotation=rotation)
        self.reset_time = reset_time
        self.button     = button
        # Initialize Hardware
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Initialize the display itself"""
        # Clear the display
        self.blank()
        # Initialize the button
        GPIO.setup(self.button, GPIO.IN)

    # End def    


    def blank(self):
        """Clear the display a black screen"""
        self.fill((0,0,0))

    # End def


    def fill(self, color):
        """Fill the display with the given color"""
        if ((color[0] < 0) or (color[0] > 255) or 
            (color[1] < 0) or (color[1] > 255) or
            (color[2] < 0) or (color[2] > 255)):
            raise ValueError("(R,G,B) must be between 0 and 255: ({0}, {1}, {2})".format(color[0], color[1], color[2]))

        self.display.fill(color565(color[0], color[1], color[2]))

    # End def


    def _get_dimensions(self, rotation):
        """Get display dimensions"""
        # Check image rotation
        if rotation % 180 == 90:
            height = self.display.width  # Swap height/width to rotate it to landscape!
            width  = self.display.height
        else:
            width  = self.display.width
            height = self.display.height
        
        return (width, height)

    # End def


    def image(self, filename, rotation=90):
        """Display the initial image on the screen"""
        # Fill display with black pixels to clear the image
        self.blank()

        # Create image with file name
        image = Image.open(filename)

        # Get screen dimensions
        width, height = self._get_dimensions(rotation)
        
        
        im_back = Image.new("RGB",(width,height))
        draw    = ImageDraw.Draw(im_back)
        draw.rectangle((0,0, width, height) , outline = 0, fill = (0,0,0)) #This is our configured rectangle, it is the background image (a black screen)
        
        

        # Scale the image to the smaller screen dimension
        image_ratio  = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width  = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width  = width
            scaled_height = image.height * width // image.width
        
        image = image.resize((int(scaled_width/4), int(scaled_height/3)), Image.BICUBIC) # resizes the image so it's easier to move around
        

        #Display the image on the background image for 
        im_back.paste(image,(0,80))
        
        self.display.image(im_back)

    def update_image(self,filename,rotation=90):
        # Create image with file name
        image = Image.open(filename)

        # Get screen dimensions
        width, height = self._get_dimensions(rotation)
        
        im_back = Image.new("RGB",(width,height))
        draw    = ImageDraw.Draw(im_back)
        draw.rectangle((0,0, width, height) , outline = 0, fill = (0,0,0)) #This is our configured rectangle, it is the background image (a black screen)
        
        
        # Scale the image to the smaller screen dimension
        image_ratio  = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width  = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width  = width
            scaled_height = image.height * width // image.width
        
        image = image.resize((int(scaled_width/4), int(scaled_height/3)), Image.BICUBIC) # resizes the image so it's easier to move around
        
        #Display the image on the background image for 
        im_back.paste(image,(0,80))
        
        self.display.image(im_back) #initiates the image
        
    # Code to update the image position with button clicks
        button_count = 0
        button_press_time = 0.0

        # Create image with file name
        while(1):
            while (GPIO.input(self.button) == 1):
                time.sleep(0.1)
                
            # Record time
            button_press_time = time.time()

            # Wait for button release
            while (GPIO.input(self.button) == 0):
                time.sleep(0.1)
            
            # Compare time to increment or reset people_count
            if (time.time() - button_press_time) > self.reset_time:
                
                image = Image.new("RGB", (width, height))
    
                # Get drawing object to draw on image.
                draw = ImageDraw.Draw(image)
                draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

                self.text(["Didi has clicked the detonator.","Game Over!"], justify=CENTER, align=CENTER, fontcolor = (255,0,0))
                time.sleep(3)
                # Will exit the game on the fail condition and display "Game Over" on the SPI Display
                return
                
            else: 
                button_count = (button_count + 1)
                t0           = time.time()
                
                if button_count == 15:
                    im_back2 = Image.new("RGB",(width,height))
                    draw    = ImageDraw.Draw(im_back2)
                    draw.rectangle((0,0, width, height) , outline = 0, fill = (0,0,0)) #This is our configured rectangle, it is the background image (a black screen)
                    im_back2.paste(image, (60,80))
                    self.display.image(im_back2)
                elif button_count == 30:
                    im_back3 = Image.new("RGB",(width,height))
                    draw    = ImageDraw.Draw(im_back3)
                    draw.rectangle((0,0, width, height) , outline = 0, fill = (0,0,0)) #This is our configured rectangle, it is the background image (a black screen)
                    im_back3.paste(image, (120,80))
                    self.display.image(im_back3)
                elif button_count == 45:
                    im_back4 = Image.new("RGB",(width,height))
                    draw    = ImageDraw.Draw(im_back4)
                    draw.rectangle((0,0, width, height) , outline = 0, fill = (0,0,0)) #This is our configured rectangle, it is the background image (a black screen)
                    im_back4.paste(image, (180,80))
                    self.display.image(im_back4)
                elif button_count == 60:
                    im_back5 = Image.new("RGB",(width,height))
                    draw    = ImageDraw.Draw(im_back5)
                    draw.rectangle((0,0, width, height) , outline = 0, fill = (0,0,0)) #This is our configured rectangle, it is the background image (a black screen)
                    im_back5.paste(image, (240,80))
                    self.display.image(im_back5)
                    self.text(["You stopped Didi.","WELL DONE!"], justify=CENTER, align=CENTER, fontcolor = (0,255,0))
                    return
                    
        
    # End def
    

    def text(self, value, fontsize=18, fontcolor=(255,255,255), 
                   backgroundcolor=(0,0,0), justify=LEFT, align=TOP, 
                   rotation=90):
                       
        """ Update the display with text
        
        :param value           : Value can be a string or list of string
        :param fontsize        : Size of font
        :param fontcolor       : (R, G, B) tuple for the color of the text
        :param backgroundcolor : (R, G, B) tuple for the color of the background
        :param justify         : Value in [LEFT, CENTER, RIGHT]
        :param align           : Value in [TOP, CENTER, BOTTOM]
        :param rotation        : Orientation of the display
        
        Will throw a ValueError 
        """
        # Debug variable
        debug = False
        
        # Check inputs:
        if justify not in [LEFT, CENTER, RIGHT]:
            raise ValueError("Input justify must be in [LEFT, CENTER, RIGHT]")
        if align not in [TOP, CENTER, BOTTOM]:
            raise ValueError("Input align must be in [TOP, CENTER, BOTTOM]")

        # Determine if text value is string or list
        #   - Rest of function assumes value is a list of strings
        if (type(value) is not list):
            value = [value]

        # Clear screen
        self.fill(backgroundcolor)
        
        # Get display dimensions
        width, height = self._get_dimensions(rotation)

        # Create a canvas for drawing
        canvas = Image.new("RGB", (width, height))

        # Get drawing object to draw on canvas
        draw   = ImageDraw.Draw(canvas)

        # Load a TTF Font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)

        # Get height of a character
        font_height = font.getsize(" ")[1]

        if (debug):
            print("Canvas h = {0}".format(height))
            print("Font   h = {0}".format(font_height))

        # Calculate number of lines supported on screen w/ font choice        
        num_line = height // font_height
        
        if (debug):
            print("Num Lines      = {0}".format(num_line))

        # Issue warning if too many lines        
        if (len(value) > num_line):
            print("WARNING:  Too many lines for font size.  Truncating.")
            print("    Required lines : {0}".format(len(value)))
            print("    Available lines: {0}".format(num_line))
            # Truncate list
            del value[num_line:]
            
        # Create list of positions for each line
        text_height = len(value) * font_height   # Number of lines * font height

        # Get initial y position
        if align == TOP:
            y = 0
        if align == BOTTOM:
            y = height - text_height
        if align == CENTER:
            y = (height // 2) - (text_height // 2) 
        
        # Adjust y position by padding
        y = y + PADDING
        
        # Only print lines there is space for
        for i, line in enumerate(value):
            # Get width of line
            line_width = font.getsize(line)[0]
            
            # Issue warning if too many characters
            if (line_width > width):
                print("WARNING:  Too many characters for the line.  Truncating.")
                print("    Required width : {0}".format(line_width))
                print("    Available width: {0}".format(width))
                # Truncate line
                for i in range(len(line)):
                    line_width = font.getsize(line[:-(i+1)])[0]
                    if (line_width <= width):
                        line = line[:-(i+1)]
                        break

            # Get x position
            if justify == LEFT:
                x = 0
            if justify == RIGHT:
                x = width - line_width
            if align == CENTER:
                x = (width // 2) - (line_width // 2) 

            # Draw the text
            draw.text((x, y), line, font=font, fill=fontcolor)
            y += font_height
        
        # Display image
        self.display.image(canvas)
        
    # End def    
    
# End class

class HT16K33():
    """ Class to manage a HT16K33 I2C display """
    bus     = None
    address = None
    command = None
    
    def __init__(self, bus, address=0x70):
        """ Initialize variables and set up display """
        self.bus     = bus
        self.address = address
        self.command = "/usr/sbin/i2cset -y {0} {1}".format(bus, address)
        
        self.setup(blink=HT16K33_BLINK_OFF, brightness=HT16K33_BRIGHTNESS_HIGHEST)
        
        self.blank()
    
    # End def
    
    def setup(self, blink, brightness):
        """Initialize the display itself"""
        # i2cset -y 1 0x70 0x21
        os.system("{0} {1}".format(self.command, (HT16K33_SYSTEM_SETUP | HT16K33_OSCILLATOR)))
        # i2cset -y 1 0x70 0x81
        os.system("{0} {1}".format(self.command, (HT16K33_BLINK_CMD | blink | HT16K33_BLINK_DISPLAYON)))
        # i2cset -y 1 0x70 0xEF
        os.system("{0} {1}".format(self.command, (HT16K33_BRIGHTNESS_CMD | brightness)))

    # End def    


    def encode(self, data, double_point=False):
        """Encode data to TM1637 format.
        
        This function will convert the data from decimal to the TM1637 data fromt
        
        :param value: Value must be between 0 and 15
        
        Will throw a ValueError if number is not between 0 and 15.
        """
        ret_val = 0
        
        try:
            if (data != CLEAR_DIGIT):
                if double_point:
                    ret_val = HEX_DIGITS[data] + POINT_VALUE
                else:
                    ret_val = HEX_DIGITS[data]
        except:
            raise ValueError("Digit value must be between 0 and 15.")
    
        return ret_val

    # End def


    def set_digit(self, digit_number, data, double_point=False):
        """Update the given digit of the display."""
        os.system("{0} {1} {2}".format(self.command, DIGIT_ADDR[digit_number], self.encode(data, double_point)))    

    # End def


    def set_digit_raw(self, digit_number, data, double_point=False):
        """Update the given digit of the display using raw data value"""
        os.system("{0} {1} {2}".format(self.command, DIGIT_ADDR[digit_number], data))    

    # End def


    def set_colon(self, enable):
        """Set the colon on the display."""
        if enable:
            os.system("{0} {1} {2}".format(self.command, COLON_ADDR, 0x02))
        else:
            os.system("{0} {1} {2}".format(self.command, COLON_ADDR, 0x00))

    # End def        


    def blank(self):
        """Clear the display to read nothing"""
        self.set_colon(False)

        self.set_digit_raw(3, 0x00)
        self.set_digit_raw(2, 0x00)
        self.set_digit_raw(1, 0x00)
        self.set_digit_raw(0, 0x00)

    # End def


    def clear(self):
        """Clear the display to read '0000'"""
        self.set_colon(False)

        self.set_digit(3, 0)
        self.set_digit(2, 0)
        self.set_digit(1, 0)
        self.set_digit(0, 0)

    # End def


    def update(self, value):
        """Update the value on the display.  
        
        This function will clear the display and then set the appropriate digits
        
        :param value: Value must be between 0 and 9999.
        
        Will throw a ValueError if number is not between 0 and 9999.
        """
        if ((value < 0) or (value > 9999)):
            raise ValueError("Value is not between 0 and 9999")
        
        self.set_digit(3, (value % 10))
        self.set_digit(2, (value // 10) % 10)
        self.set_digit(1, (value // 100) % 10)
        self.set_digit(0, (value // 1000) % 10)

    # End def
    
    def text(self, value):
        """ Update the value on the display with text
        
        :param value:  Value must have between 1 and 4 characters
        
        Will throw a ValueError if there are not the appropriate number of 
        characters or if characters are used that are not supported.
        """
        if ((len(value) < 1) or (len(value) > 4)):
            raise ValueError("Must have between 1 and 4 characters")        
        
        # Clear the display
        self.blank()

        # Set the display to the correct characters        
        for i, char in enumerate(value):
            try:
                char_value = LETTERS[char]
                self.set_digit_raw(i, char_value)
            except:
                raise ValueError("Character {0} not supported".format(char))
    
    def cleanup(self):
        # Clean up the HEX display to a message so that we know it's done
        self.set_digit(0, 13)        # "D"
        self.set_digit(1, 14)        # "E"
        self.set_digit(2, 10)        # "A"
        self.set_digit(3, 13)        # "D"

# End class

class BuzzerSound():
    
    pin       = None
    
    def __init__(self, pin):
        self.pin = pin
    
    # End def
    
    def play_tone(self, frequency, length):
        """Plays a given note for a given length."""
        PWM.start(self.pin, 30, frequency)
        time.sleep(length)
    # end def
    
    def end(self):
        PWM.stop(self.pin)
        PWM.cleanup()
    # End def
    

# End def
    
# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    import time

    delay = 2
    
    print("Test SPI Display:")
    
    #print("Create Display")
    display = SPI_Display()
   # time.sleep(delay)

    # Test Functions
    #print("Fill Black")
    display.blank()   
    time.sleep(delay)
    
    #print('Display pregame instructions')
    display.text(["Didi has stolen","Dexter's nuclear detonator!"], justify=CENTER, align=CENTER)
    time.sleep(delay+2)
    display.text(["Stop her before it's","too late!"], justify=CENTER, align=CENTER)
    time.sleep(delay)
    display.text(["Press the green button to run.", "Good Luck!"], justify=CENTER, align=CENTER)
    time.sleep(delay+2)
    
    display2 = HT16K33(1, 0x70)
    
    buzzer = BuzzerSound("P2_1")
    
    display2.update(3)
    buzzer.play_tone(330, 0.1)        # Play 330 Hz for 1 second
    buzzer.end()
    time.sleep(1)
    
    display2.update(2)
    buzzer.play_tone(330, 0.1)        # Play 330 Hz for 1 second
    buzzer.end()
    time.sleep(1)
    
    display2.update(1)
    buzzer.play_tone(330, 0.1)        # Play 330 Hz for 1 second
    buzzer.end()
    time.sleep(1)
    
    display2.text(" GO")
    buzzer.play_tone(440, 0.25)
    buzzer.end()
    time.sleep(0.75)
    
    
    display.image("dexter.jpg")
    
    display.update_image("dexter.jpg")
    buzzer.play_tone(400,0.25)
    buzzer.end()
    time.sleep(3)
    
    display.blank()
    display2.cleanup()
    
    exit()
        
    
    

