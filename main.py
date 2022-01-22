
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
pathToFile = '/home/pi/On-Off-Desktop/'
# shutdown computer ok
def shutdownComputer(ip, port, secret):
    try:
        response = requests.get("http://"+ip+":"+port+"/"+secret+"/")
    except:
        pass
def wakeOnLanComputer(macAdress):
    send_magic_packet(macAdress)

# pip install octorest
def get_printer_info_test(client):
    printing = client.printer()['state']['flags']['printing']
    return printing



def main():



    with open(pathToFile+'devices.json') as deviceFile:
        tuyaDevices = json.load(deviceFile)

        lightDevice = tuyaDevices[0]
        light = tinytuya.OutletDevice(lightDevice['id'], lightDevice['ip'], lightDevice['key'])
        light.set_version(3.3)

        printerDevice = tuyaDevices[1]
        printer = tinytuya.OutletDevice(printerDevice['id'], printerDevice['ip'], printerDevice['key'])
        printer.set_version(3.3)

        computer = tuyaDevices[2]

        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM) # Use physical pin numbering
        PIN = 26
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 26 to be an input pin and set initial value to be pulled low (off)
        # get init value
        initValue = GPIO.input(PIN)

        with open(pathToFile+'conf.json') as json_file:
            data = json.load(json_file)
            try:
                client = OctoRest(url="http://octopi.local", apikey=data['octopiApiKey'])
                client.connect()
            except Exception as e:
                print(e)
            while True: # Run forever
                value = GPIO.input(PIN)
                if value != initValue:
                    if value == 1:
                        light.set_status(False, switch=1)
                        shutdownComputer(computer['ip'], computer['port'], computer['secret'])
                        try:
                            client = OctoRest(url="http://octopi.local", apikey=data['octopiApiKey'])
                            client.connect()

                            if not get_printer_info_test(client):
                                printer.set_status(False, switch=1)
                        except Exception as e:
                            print(e)
                    else:
                        light.set_status(True, switch=1)
                        printer.set_status(True, switch=1)
                        wakeOnLanComputer(computer['mac'])
                        client.connect()

                    initValue = value

if __name__ == '__main__':
    main()
