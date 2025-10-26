from flask import Flask
app = Flask(__name__)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pinon')
def pin_on():
    GPIO.setup(16, GPIO.OUT)   # like digitalio.DigitalInOut(board.D16)
                                # and digitalio.Direction.OUTPUT
    GPIO.output(16, GPIO.HIGH) # like setting digitalio.value = True
    return 'I turned on the pin.'

@app.route('/digital/write/<pin_name>/<state>')
def digital_write(pin_name, state):
    pin = int(pin_name)
    if state.upper() in ['1', 'ON', 'HIGH']:
        GPIO.setup(pin, GPIO.OUT)   # make the pin an output
        GPIO.output(pin, GPIO.HIGH) # turn the pin on
        return 'Set pin {0} to HIGH'.format(pin_name)
    elif state.upper() in ['0', 'OFF', 'LOW']:
        GPIO.setup(pin, GPIO.OUT)   # make the pin an output 
        GPIO.output(pin, GPIO.LOW)  # turn the pin off
        return 'Set pin {0} to LOW'.format(pin_name)
    return 'Something went wrong'
