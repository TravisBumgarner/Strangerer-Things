import board
import neopixel
import random
import time

ADDRESSABLE_LEDS = 50
OFF = (0,0,0)
ON = (255,255,255)

pixels = neopixel.NeoPixel(board.D12, ADDRESSABLE_LEDS) 


def sanitize_message(text):
    # Remove bad chars
    pass


def random_color():
    # gen random tuple for a color
    pass


def render_message(text):
    letter_offset = ord('a')
    for letter in text.lower():
        index = ord(letter) - letter_offset
        pixels[index] = ON
        time.sleep(0.25)
        pixels[index] = OFF
        time.sleep(0.25 / 2)
        

def all_off():
    for led in range(ADDRESSABLE_LEDS):
        pixels[led] = OFF
        
        
def all_on(color=None):
    if color is None:
        color = ON
    for led in range(ADDRESSABLE_LEDS):
        pixels[led] = ON


def main():
    while True:
        all_off()
        render_message('ace')
        
        


if __name__ == "__main__":
    main()