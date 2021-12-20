import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs

GPIO.setmode(GPIO.GPIO) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

SWITCH = 26 #Définit le numéro du port GPIO qui alimente la led

input = GPIO.input(SWITCH)
print(input)
