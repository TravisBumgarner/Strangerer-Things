import board
import neopixel
import random
import time

import boto3

from config import region_name, aws_access_key_id, aws_secret_access_key, queue_name

###### CONSTANTS HERE #####

# COLORS & BRIGHTNESSES
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW =(255,255,0)
WHITE = ON = (255,255,255)
OFF = (0,0,0)
PS_ORANGE = (249, 104, 22)
PS_PINK = (232,10,137)


# Themes
CHRISTMAS_THEME = "CHRISTMAS_MODE"
CHRISTMAS_COLORS = [WHITE, GREEN, RED]

PS_THEME = "PS_THEME"
PS_COLORS = [PS_ORANGE, PS_PINK]

CHS_THEME = "CHS_THEME"
CHS_COLORS = [RED, BLUE, YELLOW, GREEN]

RANDOM_THEME = "RANDOM_THEME"

SELECTED_THEME = CHRISTMAS_THEME

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

alphabet_to_led = {
"a": 0,
"b": 1,
"c": 2,
"d": 3,
"e": 4,
"f": 5,
"g": 6,
"h": 7,
"i": 8,
"j": 16,
"k": 15,
"l": 14,
"m": 13,
"n": 12,
"o": 11,
"p": 10,
"q": 9,
"r": 17,
"s": 18,
"t": 19,
"u": 20,
"v": 21,
"w": 22,
"x": 23,
"y": 24,
"z": 25   
}


###### /CONSTANTS HERE #####

pixels = neopixel.NeoPixel(board.D12, ADDRESSABLE_LEDS, pixel_order=neopixel.RGB) 
sqs = boto3.resource('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
queue = sqs.get_queue_by_name(QueueName=queue_name)

def sanitize_message(text):
    sanitized_text = ''
    
    for letter in text.lower():
        if ord(letter) >= A or ord(letter) <= Z or ord(letter) == SPACE:
            sanitized_text += letter     
    return sanitized_text


def get_pixel_color(index=None):
    # index % len(possible_them_colors) gives us the index to pick
    color = None
    if SELECTED_THEME == CHRISTMAS_THEME:
        print(index % len(CHRISTMAS_COLORS))
        color = CHRISTMAS_COLORS[random.randint(0,len(CHRISTMAS_COLORS) - 1)]
        
    elif SELECTED_THEME == PS_THEME:
        color = PS_COLORS[random.randint(0,len(PS_COLORS) - 1)]
        
    elif SELECTED_THEME == CHS_THEME:
        color = CHS_COLORS[random.randint(0,len(CHS_COLORS) - 1)]
        
    elif SELECTED_THEME == RANDOM_THEME:
        r = random.randint(0,255)
        b = random.randint(0,255)
        g = random.randint(0,255)
        color = (r,g,b)
    print(color)
    return color


def render_word(word):
    letter_offset = ord('a')
      
    for letter_index, letter in enumerate(word):
        index = alphabet_to_led[letter]
        pixels[index] = get_pixel_color(letter_index) 
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
        r,b,g = get_pixel_color(i)
        pixels[i] = (int(r  * lights[i] / 4), int(b * lights[i] / 4), int(g * lights[i] / 4))


def error_mode():
    for i in range(3):
        all_on(color=RED)
        time.sleep(0.25)
        all_off()
        time.sleep(0.25)    


def main():
    message = None
    while True:
        messages = queue.receive_messages()
        if messages:
            for message in messages:   
                sanitized_message = sanitize_message(message.body)
                for _ in range(TIMES_TO_DISPLAY_MESSAGE):
                    all_off()
                    time.sleep(PAUSE_BETWEEN_MESSAGE_REPEATS)
                    render_message(sanitized_message)
                    time.sleep(PAUSE_BETWEEN_MESSAGE_REPEATS)
                message.delete()
            
        else:
            idle_mode()


if __name__ == "__main__":
    try:
        main()
    
    except Exception as e:
        print(e)
        error_mode()
    
    finally:
        all_off()