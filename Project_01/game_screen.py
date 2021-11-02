
# Import the appropriate libraries 
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------

class SPIdisp():
    """ Class to manage the SPI display"""
    cs_pin    =  None   
    dc_pin    =  None    
    reset_pin =  None
    spi       =  None
    display   =  None

    def __init__(self, cs_pin=board.P1_6, dc_pin=board.P1_4, reset_pin=board.P1_2, baudrate=24000000, rotation=90):
        
        self.cs_pin    = digitalio.DigitalInOut(cs_pin)
        self.dc_pin    = digitalio.DigitalInOut(dc_pin)
        self.reset_pin = digitalio.DigitalInOut(reset_pin)
        self.spi       = board.SPI()
        self.display   = ili9341.ILI9341(self.spi, self.cs_pin, self.dc_pin, self.reset_pin, 
                                         baudrate=baudrate, rotation=rotation)
                                         
        self.setup() 
     # End def

    def setup(self):
        # Make sure to create image with mode 'RGB' for full color
        if self.display.rotation % 180 == 90:
            height = self.display.width  # we swap height/width to rotate it to landscape!
            width  = self.display.height
        else:
            width  = self.display.width  # we swap height/width to rotate it to landscape!
            height = self.display.height
            
        #Sets up the LCD screen display
        image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box as the background
        draw.rectangle((0, 0, width, height), fill=(0, 255, 0))
        
        self.display.image(image)
        
        time.sleep(1)


    def display_text(self, text, size, rotation):
        # This function takes the string it is fed and displays it
        
        if (len(text) > 50):
            print("Text too long for display")
            return
    
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if self.display.rotation % 180 == 90:
            height = self.display.width  # we swap height/width to rotate it to landscape!
            width  = self.display.height
        else:
            width  = self.display.width  # we swap height/width to rotate it to landscape!
            height = self.display.height

        image = Image.new("RGB", (width, height))
    
       # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
    
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        self.display.image(image)
    
        # Load a TTF Font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        
        (font_width, font_height) = font.getsize(text)
        draw.text((width // 2 - font_width // 2, height // 2 - font_height // 2),text,font=font,fill=(255, 255, 255),)

        self.display.image(image)
    
    
    # End def
# End class


if __name__ == "__main__":
    import time

    print("Testing SPI Display")
    display = SPIdisp()
    
    print("Display instantiated")
    
    time.sleep(2)
    
    print("Display text")
    # Test text()
    text = "Hello World !"
    size = 20
    rotation = 90
    #display.display_text(text,size,rotation)
    
    time.sleep(2)
    
    # Test next function
    # ....

