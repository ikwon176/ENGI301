"""
--------------------------------------------------------------------------
Display News Headlines and Daily Weather Forecast on LCD Screen
--------------------------------------------------------------------------
License:   
Copyright 2019 Irene Kwon

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
    
    * adafruit_rgb_display
        * used to interface ILI9341 LCD Screen with PocketBeagle
    * Adafruit_Blinka
        * used for circuit python to then use digitalio
  
--------------------------------------------------------------------------
Background Information: 
 
    * Base code/instructions:
        * https://learn.adafruit.com/adafruit-2-dot-8-color-tft-touchscreen-breakout-v2/python-wiring-and-setup

--------------------------------------------------------------------------
Outline:
    
    - Set up the PocketBeagle and LCD screen
    - Import/use the functions to gather the necessary data
    - Display text on LCD screen
    - Control display with button
    
"""
# ------------------------------------------------------------------------------
# Setup for LCD Display/Interfacing with Display
# ------------------------------------------------------------------------------

#Import necessary libraries
import os
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341


#Define the CS, DC, and Reset pins
cs_pin    = digitalio.DigitalInOut(board.P2_2)
dc_pin    = digitalio.DigitalInOut(board.P2_4)
reset_pin = digitalio.DigitalInOut(board.P2_6)

# Config for display baudrate (default max is 24mhz):
BAUDRATE  = 24000000

# Setup the SPI bus
spi       = board.SPI()

# Create the display
disp      = ili9341.ILI9341(spi, rotation=90, 
                            cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)


# ------------------------------------------------------------------------------
# Setup Button
# ------------------------------------------------------------------------------

import time
import Adafruit_BBIO.GPIO as GPIO

BUTTON0    = "P2_8"

# ------------------------------------------------------------------------------
# Setup FinalNews.py and FinalWeather.py and Outputs Desired
# ------------------------------------------------------------------------------

import FinalNews
import FinalWeather
import textwrap
 
DH_raw      = str(FinalWeather.high)
DL_raw      = str(FinalWeather.low)
DC_raw      = str(FinalWeather.curr)

News_Header = str(FinalNews.header)
Article     = FinalNews.article
News_Info   = News_Header.splitlines()

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

def setup():
    GPIO.setup(BUTTON0, GPIO.IN)
    print("Setup Complete")
    
# End def

def setup_wifi():
    os.system("connmanctl enable wifi")
    os.system("connmanctl agent on")
    os.system("connmanctl connect wifi_74da38de508b_526963652056697369746f72_managed_none")
# End def

            
# For displaying on the LCD Screen
def cleanstring(string):
    cleana = string.replace("(", "")
    cleanb = cleana.replace(")", "")
    cleanc = cleanb.replace("'", "")
    cleand = cleanc.replace(",", "")
    
    def createRGB(disp):
        
        if disp.rotation % 180 == 90:
            height = disp.width   # we swap height/width to rotate it to landscape!
            width  = disp.height
        else:
            width  = disp.width   # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new('RGB', (width, height))
     
        # Reset the screen to black
        draw = ImageDraw.Draw(image)
        
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)
        
        # Display the desired output
        if ("Headlines" in cleand):
            size = 16
        else:
            size = 20
            
        fnt = ImageFont.truetype('Pillow-master/Tests/fonts/FreeMono.ttf', size)
        
        draw.text((0,0), text=cleand, fill = (255,255,255), font=fnt)
        disp.image(image)
        
    return createRGB(disp)
    # End def
# End def

def WeatherUpdate(DL_raw, DH_raw, DC_raw):
    temps     = [DC_raw, DL_raw, DH_raw][0:]
    all_temps = "\n".join(temps)
    cleanstring(all_temps)
    
# End def

def NewsUpdate(News_Info, Article):
    newslist = News_Info + Article
    news     = newslist[1:]
    all_news    = "\n".join(news)
    cleanstring(all_news)
    
def task():
    initialize        = True
    button_press      = 0
    button_press_time = 0.0
    
    while(1):
        try:
            # Wait for button press
            #print("Here")
            while(GPIO.input(BUTTON0) == 1):
    #            print("Here1")
                pass #don't do anything if 1, just keep coming back to check condition
            
            # Record time
            button_press_time = time.time()
            
            # Wait for button release
            while(GPIO.input(BUTTON0) == 0):
                pass
            
            # If instantaneously pressed (ie less than 2)
            if ((time.time() - button_press_time) > 2.0): #if beyond 2 seconds
                exit() #exits out of script
            else:
                button_press += 1
    #            print(button_press)
                #Times the button is pressed: display news (even) or weather (odd)
                
                # Run on the first button press to initialize the wifi
                if initialize:
                    setup_wifi()
                    initialize = False
                    
                if (button_press % 2) == 1:
                    WeatherUpdate(DL_raw, DH_raw, DC_raw)
                else:
                    NewsUpdate(News_Info, Article)
        except:
            pass

# End def

#-------------------------------------------------------------------------------
# Main Script
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    
    setup()
    try:
        task()
    except KeyboardInterrupt:
        pass