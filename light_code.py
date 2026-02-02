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
    percent = max(0, min(100, percent))
    level = int(percent / 100.0 * 65535)
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

def stacking_mode(delay=0.3, fade_duration=0.2):
    """Stacks lights from 1st floor to 9th floor with fade-in."""
    print("Mode: Stacking")
    clear_all()
    for i in range(NUM_FLOORS):
        fade_in(i, duration=fade_duration)
        time.sleep(delay)
    time.sleep(0.5)
    # Fade all out slowly
    steps = 20
    for s in range(steps + 1):
        brightness = 100 - (s / steps) * 100
        for i in range(NUM_FLOORS):
            set_brightness(i, brightness)
        time.sleep(0.5 / steps)
    time.sleep(0.5)

def wave_mode(delay=0.05, wave_width=2):
    """A 'stadium wave' moving up and down."""
    print("Mode: Stadium Wave")
    # Move up
    # Iterate through positions from -wave_width to NUM_FLOORS + wave_width
    for p in [x * 0.5 for x in range(0, int((NUM_FLOORS + wave_width) * 2))]:
        for i in range(NUM_FLOORS):
            # Calculate distance from pulse center p
            dist = abs(i - p)
            if dist < wave_width:
                brightness = (1 - dist / wave_width) * 100
            else:
                brightness = 0
            set_brightness(i, brightness)
        time.sleep(delay)
    
    # Move down
    for p in [x * 0.5 for x in range(int((NUM_FLOORS + wave_width) * 2), -1, -1)]:
        for i in range(NUM_FLOORS):
            dist = abs(i - p)
            if dist < wave_width:
                brightness = (1 - dist / wave_width) * 100
            else:
                brightness = 0
            set_brightness(i, brightness)
        time.sleep(delay)
    clear_all()

def all_blink(count=5, fade_in_duration=0.3, fade_out_duration=0.3, pause=0.2):
    """Blinks all floors simultaneously with fade in and out."""
    print("Mode: All Blink (Fade)")
    for _ in range(count):
        # Fade In All
        steps = 15
        for s in range(steps + 1):
            brightness = (s / steps) * 100
            for i in range(NUM_FLOORS):
                set_brightness(i, brightness)
            time.sleep(fade_in_duration / steps)
        
        time.sleep(pause)
        
        # Fade Out All
        for s in range(steps + 1):
            brightness = 100 - (s / steps) * 100
            for i in range(NUM_FLOORS):
                set_brightness(i, brightness)
            time.sleep(fade_out_duration / steps)
        
        time.sleep(pause)

def main():
    try:
        while True:
            stacking_mode(delay=0.2, fade_duration=0.3)
            time.sleep(1)
            wave_mode(delay=0.05, wave_width=2.5)
            time.sleep(1)
            all_blink(count=3, fade_in_duration=0.5, fade_out_duration=0.5)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        clear_all()
        pca.reset()
        pca.deinit()

if __name__ == "__main__":
    main()

