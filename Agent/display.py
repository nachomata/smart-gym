import time,sys
import grovepi

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import random
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap)
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Update the display without erasing the display
def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

# Create a custom character (from array of row patterns)
def create_char(location, pattern):
    """
    Writes a bit pattern to LCD CGRAM

    Arguments:
    location -- integer, one of 8 slots (0-7)
    pattern -- byte array containing the bit pattern, like as found at
               https://omerk.github.io/lcdchargen/
    """
    location &= 0x07 # Make sure location is 0-7
    textCommand(0x40 | (location << 3))
    bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, pattern)

# example code
if __name__=="__main__":
    setText("Hello world\nThis is an LCD test")
    setRGB(0,128,64)
    time.sleep(2)
    # for c in range(0,255):
    #     setText_norefresh("Going to sleep in {}...".format(str(c)))
    #     setRGB(c,255-c,0)
    #     time.sleep(0.1)
    setRGB(0,255,0)
    setText("Bye bye, this should wrap onto next line")
    
    beautiful_colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
    setText("Test")

    while True:
        # Generate a random color from the beautiful_colors list
        color = random.choice(beautiful_colors)
        
        # Set the RGB values based on the selected color
        if color == "red":
            setRGB(255, 0, 0)
        elif color == "orange":
            setRGB(255, 165, 0)
        elif color == "yellow":
            setRGB(255, 255, 0)
        elif color == "green":
            setRGB(0, 255, 0)
        elif color == "blue":
            setRGB(0, 0, 255)
        elif color == "purple":
            setRGB(128, 0, 128)
        elif color == "pink":
            setRGB(255, 192, 203)
        
        # Set the text to "Kyle is beautiful"
        
        
        # Wait for 2 seconds before changing the color and text
        time.sleep(1)