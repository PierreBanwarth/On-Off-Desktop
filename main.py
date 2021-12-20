
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

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
