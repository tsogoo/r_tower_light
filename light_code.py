import board
import busio
import time
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.reset()
pca.frequency = 1000

def set_brightness(k, percent):
    level = int((1.0 - (percent/100.0))*65535)
    pca.channels[k].duty_cycle = level

def fade_in(i, step = 4, brightness=100):
    for j in range(100, 1, -1):
        set_brightness(i,j)
        time.sleep(0.01)

def fade_out(i, step = 4, brightness=100):
    for j in range(0, 100, 100/4):
        set_brightness(i,j)
        time.sleep(0.01)

for i in range(0, 100):
    fade_in(0, 4)
    fade_out(0, 4)
pca.reset()
pca.deinit()
