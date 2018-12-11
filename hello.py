import board
import neopixel
import random
import time


pixels = neopixel.NeoPixel(board.D12, 50) # Raspberry Pi wiring!

pixels[0] = (255,0,0)

for i in range(0,50):
    # pixels[i] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    pixels[i] = (0,0,255)
    time.sleep(0.1)

