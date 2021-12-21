
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import requests
import json
from wakeonlan import send_magic_packet
from octorest import OctoRest
import tinytuya

# https://pypi.org/project/tinytuya/
# pip install tinytuya
# Online management of on/off switchs for 3D printer and Light (futur for screens too)

# a dictionary
macAdressTest = 'ff.ff.ff.ff.ff.ff'

# shutdown computer ok
def shutdownComputer():
    response = requests.get("http://192.168.1.108:5001/popote/")
    print(response)

def wakeOnLanComputer(macAdress):
    send_magic_packet(macAdress)

# pip install octorest


def get_printer_info_test(octopiApiKey):
    try:
        client = OctoRest(url="http://octopi.local", apikey=octopiApiKey)
        printing = client.printer()['state']['flags']['printing']
        return printing
    except Exception as e:
        print(e)



def main():
    light = tinytuya.OutletDevice('bf613851c9c697820fgwqt', '192.168.1.89', '3b41fcf6ca71d0ae')
    light.set_version(3.3)

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    PIN = 26
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 26 to be an input pin and set initial value to be pulled low (off)
    # get init value
    initValue = GPIO.input(PIN)

    with open('conf.json') as json_file:
        data = json.load(json_file)
        while True: # Run forever
            value = GPIO.input(PIN)
            if value != initValue:
                test = get_printer_info_test(data['octopiApiKey'])
                if(test):
                    print('''Currently Printing don't turn off''')
                else:
                    print('''Turn off 3D print ''')
                if value == 1:
                    print('off')
                    light.set_status(off, switch=1)
                else:
                    print('on')
                    light.set_status(on, switch=1)
                initValue = value

if __name__ == '__main__':
    main()
