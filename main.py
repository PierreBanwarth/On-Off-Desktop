
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import requests
from wakeonlan import send_magic_packet
from octorest import OctoRest

# https://pypi.org/project/tinytuya/
# pip install tinytuya
# Online management of on/off switchs for 3D printer and Light (futur for screens too)


macAdressTest = 'ff.ff.ff.ff.ff.ff'



# shutdown computer ok
def shutdownComputer():
    response = requests.get("http://192.168.1.108:5001/popote")
    print response

def wakeOnLanComputer(macAdress):
    send_magic_packet(macAdress)

# pip install octorest
def get_printer_info():
    try:
        client = OctoRest(url="http://octopi.local", apikey="YouShallNotPass")
        message = ""
        message += str(client.version) + "\n"
        message += str(client.job_info()) + "\n"
        printing = client.printer()['state']['flags']['printing']
        if printing:
            message += "Currently printing!\n"
        else:
            message += "Not currently printing...\n"
        return message
    except Exception as e:
        print(e)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
PIN = 26
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 26 to be an input pin and set initial value to be pulled low (off)

shutdown = False
while True: # Run forever
    value = GPIO.input(PIN)

    if value == 1 and not shutdown:
        shutdownComputer()
        shutdown = True
