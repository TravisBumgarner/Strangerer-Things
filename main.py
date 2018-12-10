import board
import neopixel
import random
import time

ADDRESSABLE_LEDS = 50
OFF = (0,0,0)
WHITE = (255,255,255)
RED = (0, 255, 0)

pixels = neopixel.NeoPixel(board.D12, ADDRESSABLE_LEDS) 


def sanitize_message(text):
    sanitized_text = ''
    
    for letter in text.lower():
        if ord(letter) < ord('a') or ord(letter) > ord('z'):
            continue
        sanitized_text += letter
    return sanitized_text


def random_color():
    # gen random tuple for a color
    pass


def render_message(text):
    letter_offset = ord('a')
    for letter in text:
        index = ord(letter) - letter_offset
        pixels[index] = WHITE
        time.sleep(0.25)
        pixels[index] = OFF
        time.sleep(0.25 / 2)
        

def all_off():
    for led in range(ADDRESSABLE_LEDS):
        pixels[led] = OFF
        
        
def all_on(color=None):
    if color is None:
        color = WHITE
    for led in range(ADDRESSABLE_LEDS):
        print(led)
        pixels[led] = color


def main():
    try:
        while True:
            message = 'CART!'
            sanitized_message = sanitize_message(message)
            render_message(sanitized_message)
    except:
        #print(e)
        for i in range(3):
            all_on(color=RED)
            time.sleep(0.25)
            all_off()
            time.sleep(0.25)    
        raise
        


if __name__ == "__main__":
    main()