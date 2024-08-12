# Please modify to meet your application
WEB_ADDRESS = "YOUR_WEBSITE.COM/YOUR_PROJECT_PATH/picture_generator.php?auth_token=YOUR_AUTH_TOKEN"

# Original import statements
print("Application Opened. Loading imports...")

from gpiozero import Button, LED
import time
import threading
import asyncio
import subprocess
from subprocess import check_call

led = LED(14)

# Function to blink LED with a specified pattern
def blink_led(pattern, repeat=1):
    for i in range(repeat):
        for symbol in pattern:
            if symbol == '.':
                led.on()
                time.sleep(0.2)  # Short blink
            elif symbol == '-':
                led.on()
                time.sleep(0.5)  # Long blink
            elif symbol == ' ':
                led.off()
                time.sleep(0.2)  # Short pause
            led.off()
            time.sleep(0.2)

# Function to dynamically change LED pattern
def set_led_pattern(new_pattern, new_status):
    global current_pattern, status
    current_pattern = new_pattern
    status = new_status

# Initialize LED pattern
current_pattern = "."
status = "loading"

# Function to blink LED on a separate thread
def blink_led_thread():
    while status != "error":
        blink_led(current_pattern)

    blink_led(current_pattern, 5)

# Start LED blinking thread
led_thread = threading.Thread(target=blink_led_thread)
led_thread.start()

from Adafruit_Thermal import *
from PIL import Image
import io
import requests

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
set_led_pattern(" ", "connected")

finished_printing = True
def button_callback():
    global finished_printing
    if finished_printing:
        finished_printing = False
        print("Button pressed!")
        set_led_pattern(".", "loading")  # Indicate loading
        capture_and_print_screenshot()

def capture_and_print_screenshot():
    global finished_printing, WEB_ADDRESS
    try:
        # Send a GET request to the URL
        response = requests.get(WEB_ADDRESS)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
                # Access the content of the response (image data in bytes)
                image_data = io.BytesIO(response.content)
                img = Image.open(image_data)
                printer.printImage(img, True) # This does the printing
        else:
                set_led_pattern(".-.   ", "semi_error")
                print('Failed to download image. Status code:', response.status_code)
                time.sleep(10)
        
        finished_printing = True
        set_led_pattern(" ", "sucess")  # Indicate successful print

    except Exception as e:
        set_led_pattern("...-   ", "error")  # Indicate error
        raise SystemExit("an Error occured")


def shutdown():
    set_led_pattern(".- ", "shutting down")
    time.sleep(5)
    check_call(['sudo', 'poweroff'])

button = Button(3, hold_time=2)
button.when_pressed = button_callback
button.when_held = shutdown

try:
    print("Press the button connected to GPIO 3 to print the poem.")
    while status != "error":
        time.sleep(1)  # Keep the script running to detect button press

except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    GPIO.cleanup()  # Clean up GPIO on script exit
