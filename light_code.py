import board
import busio
import time
from adafruit_pca9685 import PCA9685

# Configuration
NUM_FLOORS = 9
FLOOR_CHANNELS = list(range(NUM_FLOORS))  # Assuming channels 0-8 for 9 floors

# Initialize I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.reset()
pca.frequency = 1000

def set_brightness(channel, percent):
    """Sets brightness from 0 to 100. Inverts duty cycle as per original logic."""
    # Ensure percent is between 0 and 100
    percent = max(0, min(100, percent))
    # Original logic: 100% brightness -> 0 duty cycle, 0% -> 65535
    level = int((1.0 - (percent / 100.0)) * 65535)
    pca.channels[channel].duty_cycle = level

def clear_all():
    """Turns off all floor lights."""
    for channel in FLOOR_CHANNELS:
        set_brightness(channel, 0)

def fade_in(channel, duration=0.5):
    """Smoothly fades in a single channel."""
    steps = 20
    for i in range(steps + 1):
        brightness = (i / steps) * 100
        set_brightness(channel, brightness)
        time.sleep(duration / steps)

def fade_out(channel, duration=0.5):
    """Smoothly fades out a single channel."""
    steps = 20
    for i in range(steps + 1):
        brightness = 100 - (i / steps) * 100
        set_brightness(channel, brightness)
        time.sleep(duration / steps)

def stacking_mode(delay=0.3):
    """Stacks lights from 1st floor to 9th floor."""
    print("Mode: Stacking")
    clear_all()
    for i in range(NUM_FLOORS):
        set_brightness(i, 100)
        time.sleep(delay)
    time.sleep(0.5)
    clear_all()
    time.sleep(0.5)

def wave_mode(delay=0.1):
    """A light wave moving up and down."""
    print("Mode: Wave")
    # Move up
    for i in range(NUM_FLOORS):
        set_brightness(i, 100)
        if i > 0:
            set_brightness(i-1, 0)
        time.sleep(delay)
    # Move down
    for i in range(NUM_FLOORS - 1, -1, -1):
        set_brightness(i, 100)
        if i < NUM_FLOORS - 1:
            set_brightness(i+1, 0)
        time.sleep(delay)
    set_brightness(0, 0)

def all_blink(count=5, delay=0.3):
    """Blinks all floors simultaneously."""
    print("Mode: All Blink")
    for _ in range(count):
        for i in range(NUM_FLOORS):
            set_brightness(i, 100)
        time.sleep(delay)
        clear_all()
        time.sleep(delay)

def main():
    try:
        while True:
            stacking_mode()
            time.sleep(1)
            wave_mode()
            time.sleep(1)
            all_blink()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        clear_all()
        pca.reset()
        pca.deinit()

if __name__ == "__main__":
    main()

