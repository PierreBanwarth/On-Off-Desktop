
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
macAdress = '1C:6F:65:D1:EA:27'

# shutdown computer ok
def shutdownComputer():
    try:
        response = requests.get("http://192.168.1.108:5001/popote/")
        print(response)
    except:
        pass
def wakeOnLanComputer():
    send_magic_packet(macAdress)

# pip install octorest


def get_printer_info_test(client):
        printing = client.printer()['state']['flags']['printing']
        return printing



def main():



    with open('devices.json') as deviceFile:
        tuyaDevices = json.load(deviceFile)

        lightDevice = tuyaDevices[0]
        light = tinytuya.OutletDevice(lightDevice['id'], '192.168.1.89', lightDevice['key'])
        light.set_version(3.3)

        printerDevice = tuyaDevices[2]
        printer = tinytuya.OutletDevice(printerDevice['id'], '192.168.1.89', printerDevice['key'])
        printer.set_version(3.3)


    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    PIN = 26
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 26 to be an input pin and set initial value to be pulled low (off)
    # get init value
    initValue = GPIO.input(PIN)

    with open('conf.json') as json_file:
        data = json.load(json_file)
        try:
            client = OctoRest(url="http://octopi.local", apikey=data['octopiApiKey'])
            client.connect()
        except Exception as e:
            print(e)
        while True: # Run forever
            value = GPIO.input(PIN)
            if value != initValue:
                testPrinter = get_printer_info_test(client)

                if value == 1:
                    print('off')
                    light.set_status(False, switch=1)
                    shutdownComputer()
                    if not testPrinter:
                        printer.set_status(False, switch=1)
                else:
                    print('on')
                    light.set_status(True, switch=1)
                    printer.set_status(True, switch=1)
                    time.sleep(15)
                    client.connect()
                    wakeOnLanComputer()

                initValue = value

if __name__ == '__main__':
    main()
