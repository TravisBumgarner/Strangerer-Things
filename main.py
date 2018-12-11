import board
import neopixel
import random
import time


###### CONSTANTS HERE #####

# COLORS & BRIGHTNESSES
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = ON = (255,255,255)
OFF = (0,0,0)
PS_ORANGE = (249, 104, 22)
PS_PINK = (232,10,137)

# TIMING (ALL IN SECONDS) & LOOPING 
TIMES_TO_DISPLAY_MESSAGE = 3
PAUSE_BETWEEN_MESSAGE_REPEATS = 0.5
PAUSE_BETWEEN_WORDS = 1
PAUSE_LETTER_ON = 0.25
PAUSE_LETTER_OFF = PAUSE_LETTER_ON / 2

# HARDWARE CONFIG
ADDRESSABLE_LEDS = 50

# ORDS
A = ord('a')
Z = ord('z')
SPACE = ord(' ')

###### /CONSTANTS HERE #####

pixels = neopixel.NeoPixel(board.D12, ADDRESSABLE_LEDS, pixel_order=neopixel.RGB) 


def sanitize_message(text):
    sanitized_text = ''
    
    for letter in text.lower():
        if ord(letter) >= A or ord(letter) <= Z or ord(letter) == SPACE:
            sanitized_text += letter     
    return sanitized_text


def random_color():
    # gen random tuple for a color
    pass

def render_word(word):
    letter_offset = ord('a')
      
    for letter in word:
        index = ord(letter) - letter_offset
        even = index % 2
        pixels[index] = PS_ORANGE if even else PS_PINK 
        time.sleep(PAUSE_LETTER_ON)
        pixels[index] = OFF
        time.sleep(PAUSE_LETTER_OFF)


def render_message(text):
    words = text.split(' ')
    word_count = len(words)
    
    for word in words:
        render_word(word)
        if word_count > 1:
            time.sleep(PAUSE_BETWEEN_WORDS)
            
        
def all_off():
    for led in range(ADDRESSABLE_LEDS):
        pixels[led] = OFF
        
        
def all_on(color=None):
    if color is None:
        color = WHITE
    for led in range(ADDRESSABLE_LEDS):
        pixels[led] = color


def adjust_brightness(rgb, brightness=1):
    if brightness < 0 or brightness > 1:
        raise ValueError('Brightness is a value between 0 and 1') 

    r,g,b = rgb
    
    modified_r = int(r * brightness / 255)
    modified_g = int(g * brightness / 255)
    modified_b = int(b * brightness / 255)
    
    return (modified_r, modified_g, modified_b)


def idle_mode():
    # This function needs help
    lights = [random.randint(0,4) for i in range(ADDRESSABLE_LEDS)]
    indices = sorted([i for i in range(ADDRESSABLE_LEDS)], key=lambda *args: random.random())
    for i in indices:
        rand_r = random.randint(0,255)
        rand_b = random.randint(0,255)
        rand_g = random.randint(0,255)
        pixels[i] = (int(rand_r  * lights[i] / 4), int(rand_b * lights[i] / 4), int(rand_g * lights[i] / 4))

def error_mode():
    for i in range(3):
        all_on(color=RED)
        time.sleep(0.25)
        all_off()
        time.sleep(0.25)    


def prompt_user_input():
    try:
        return input('Enter a message to display:\n')
    except Exception as e:
        print(e)
        return None


def main():
    message = None
    while True:
                
        if message:
            all_off()
            sanitized_message = sanitize_message(message)
            for _ in range(TIMES_TO_DISPLAY_MESSAGE):
                render_message(sanitized_message)
                time.sleep(PAUSE_BETWEEN_MESSAGE_REPEATS)
            message = None
        
        else:
            try:
                while True:
                    idle_mode()
            except KeyboardInterrupt:
                message = prompt_user_input()
                print('erroring...')
                continue


if __name__ == "__main__":
    try:
        main()
    
    except Exception as e:
        print(e)
        error_mode()
    
    finally:
        all_off()