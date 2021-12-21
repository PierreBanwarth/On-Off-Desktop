
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import requests
from wakeonlan import send_magic_packet
from octorest import OctoRest


macAdressTest = 'ff.ff.ff.ff.ff.ff'
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 26 to be an input pin and set initial value to be pulled low (off)


while True: # Run forever


    if GPIO.input(26) == GPIO.HIGH:
        print("high")

        time.sleep(0.5)

    else:
        print("low")

        time.sleep(0.5)


# https://pypi.org/project/tinytuya/
# pip install tinytuya
# Online management of on/off switchs for 3D printer and Light (futur for screens too)





# shutdown computer ok
def shutdownComputer():
    response = requests.get("http://remote-host-name:5001/secret/")

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
