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
    
def repeat_last_command_or_time_out(self):
    import time

    now = time.time()
    if (now - self.last_command_time) > self.__class__.TIMEOUT_INTERVAL:
        self.timed_out = True
        return
    self.send_command_string(self.last_command_string)

def send_command(self, left, right):
    import time
    import libservo
    if (abs(left) > MAX_SPEED) or (abs(right) > MAX_SPEED):
        raise ValueError("Motor command out of range")

    self.last_command_time = time.time()
    self.timed_out = False

    command_string = "!M %d %d\r" % (-right, left)
    #self.send_command_string(command_string)
    libservo.set_target_speed(1, -right)
    libservo.set_target_speed(2, -left)

def interpret_joystick_command(x, y):
    """Accepts a joystick position (x, y) where x and y represent a point within the unit circle.
       Returns a tuple (left, right) of the corresponding motor speeds for a left and right motor in
       a differential drive setup. This code was originally written by Richard Klancer around 2012."""

    from math import atan2, sin, cos, pi, sqrt
    angle = atan2(y, x) - pi/4

    # interpret the distance from the center
    speed = sqrt(x*x + y*y)
    if speed > 1.0:
        raise ValueError("Joystick input outside the unit circle")

    left = sin(angle)
    right = cos(angle)
    # scale the motor speeds so that, if the joystick is pushed to its maximum distance from the
    # center, the faster motor is at max speed regardless of the angle
    scale = MAX_SPEED * speed / max(abs(left), abs(right))
    return (int(scale * left + 0.5), int(scale * right + 0.5))

@app.route('/joystick', methods=['POST'])
def joystick():
    x = float(request.form['x'])
    y = float(request.form['y'])
    motor.send_command(*interpret_joystick_command(x, y))
    return "ok"

import time
GPIO.setup(12, GPIO.OUT)

pin = GPIO.PWM(12, 500)  # channel=12; frequency=500Hz
pin.start(0)            # initializes the duty cycle at 0; (0.0 <= duty cycle <= 100.0)

while True:
    pin.ChangeDutyCycle(25)  # changes the duty cycle to 25% (quarter power)
    time.sleep(3)
    pin.ChangeDutyCycle(50)  # changes the duty cycle to 50% (half power)
    time.sleep(3)
    pin.ChangeDutyCycle(100) # changes the duty cycle to 100% (full power)
    time.sleep(3)
