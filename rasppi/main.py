import board
import neopixel
import random
import time
import json
import collections

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
CHRISTMAS_THEME = "CHRISTMAS_THEME"
CHRISTMAS_COLORS = [WHITE, GREEN, RED]

PS_THEME = "PS_THEME"
PS_COLORS = [PS_ORANGE, PS_PINK]

RGBY_THEME = "RGBY_THEME"
RGBY_COLORS = [RED, BLUE, YELLOW, GREEN]

RANDOM_THEME = "RANDOM_THEME"

# TIMING (ALL IN SECONDS) & LOOPING 
TIMES_TO_DISPLAY_MESSAGE = 2
PAUSE_BETWEEN_MESSAGE_REPEATS = 1.5
PAUSE_BETWEEN_WORDS = 0.75
PAUSE_LETTER_ON = 0.75
PAUSE_LETTER_OFF = PAUSE_LETTER_ON / 4

# HARDWARE CONFIG
ADDRESSABLE_LEDS = 26

# ORDS
A = ord('a')
Z = ord('z')
SPACE = ord(' ')

alphabet_to_led = collections.OrderedDict()
alphabet_to_led["a"] = 0
alphabet_to_led["b"] = 1
alphabet_to_led["c"] = 2
alphabet_to_led["d"] = 3
alphabet_to_led["e"] = 4
alphabet_to_led["f"] = 5
alphabet_to_led["g"] = 6
alphabet_to_led["h"] = 7
alphabet_to_led["i"] = 8
alphabet_to_led["j"] = 16
alphabet_to_led["k"] = 15
alphabet_to_led["l"] = 14
alphabet_to_led["m"] = 13
alphabet_to_led["n"] = 12
alphabet_to_led["o"] = 11
alphabet_to_led["p"] = 10
alphabet_to_led["q"] = 9
alphabet_to_led["r"] = 17
alphabet_to_led["s"] = 18
alphabet_to_led["t"] = 19
alphabet_to_led["u"] = 20
alphabet_to_led["v"] = 21
alphabet_to_led["w"] = 22
alphabet_to_led["x"] = 23
alphabet_to_led["y"] = 24
alphabet_to_led["z"] = 25 



###### /CONSTANTS HERE #####

pixels = neopixel.NeoPixel(board.D12, ADDRESSABLE_LEDS, pixel_order=neopixel.RGB) 
sqs = boto3.resource('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
queue = sqs.get_queue_by_name(QueueName=queue_name)

def sanitize_message(text):
    sanitized_text = ''
    
    for letter in text.lower():
        if (ord(letter) >= A and ord(letter) <= Z) or ord(letter) == SPACE:
            sanitized_text += letter     
    return sanitized_text


def get_pixel_color(index=None, theme=CHRISTMAS_THEME):   
    color = None
    if theme == CHRISTMAS_THEME:
        color = CHRISTMAS_COLORS[random.randint(0,len(CHRISTMAS_COLORS) - 1)]
        
    elif theme == PS_THEME:
        color = PS_COLORS[random.randint(0,len(PS_COLORS) - 1)]
        
    elif theme == RGBY_THEME:
        color = RGBY_COLORS[random.randint(0,len(RGBY_COLORS) - 1)]
        
    elif theme == RANDOM_THEME:
        r = random.randint(0,255)
        b = random.randint(0,255)
        g = random.randint(0,255)
        color = (r,g,b)
        
    else:
        r = random.randint(0,255)
        b = random.randint(0,255)
        g = random.randint(0,255)
        color = (r,g,b)
        
    return color


def render_word(word, theme):
    letter_offset = ord('a')
      
    for letter_index, letter in enumerate(word):
        index = alphabet_to_led[letter]
        pixels[index] = get_pixel_color(letter_index, theme) 
        time.sleep(PAUSE_LETTER_ON)
        pixels[index] = OFF
        time.sleep(PAUSE_LETTER_OFF)


def render_message(text, theme):
    words = text.split(' ')
    word_count = len(words)
    for word in words:
        render_word(word, theme)
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
    
    modified_r = int(r * brightness)
    modified_g = int(g * brightness)
    modified_b = int(b * brightness)
    
    return (modified_r, modified_g, modified_b)


def idle_mode():
    # This function needs help
    lights = [random.randint(0,4) for i in range(ADDRESSABLE_LEDS)]
    indices = sorted([i for i in range(ADDRESSABLE_LEDS)], key=lambda *args: random.random())
    for i in indices:
        r,b,g = get_pixel_color(i, RANDOM_THEME)
        pixels[i] = (int(r  * lights[i] / 4), int(b * lights[i] / 4), int(g * lights[i] / 4))


def message_incoming_mode():
    all_off()
    for i in alphabet_to_led.values():
        pixels[i] = get_pixel_color(i, RANDOM_THEME)
        time.sleep(0.15)
    all_off()

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
                parsed_message = json.loads(message.body)
                sanitized_message = sanitize_message(parsed_message["content"])
                print('Incoming message: ' + sanitized_message)
                theme = parsed_message["colors"]
                message_incoming_mode()
                for _ in range(TIMES_TO_DISPLAY_MESSAGE):
                    all_off()
                    time.sleep(PAUSE_BETWEEN_MESSAGE_REPEATS)
                    render_message(sanitized_message, theme)
                    time.sleep(PAUSE_BETWEEN_MESSAGE_REPEATS)
                message.delete()
            
        else:
            idle_mode()


if __name__ == "__main__":
    try:
        main()
    
    except Exception as e:
        print('exception', e)
        error_mode()
    
    finally:
        all_off()