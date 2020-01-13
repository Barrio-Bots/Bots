from digitalio import DigitalInOut, Pull, Direction
from adafruit_crickit import crickit
import board

# Two onboard CPX buttons for input (low level saves memory)
button_a = DigitalInOut(board.BUTTON_A)
button_a.direction = Direction.INPUT
button_a.pull = Pull.DOWN

button_b = DigitalInOut(board.BUTTON_B)
button_b.direction = Direction.INPUT
button_b.pull = Pull.DOWN

# Create one motor on seesaw motor port #1
motor = crickit.dc_motor_1


def start_motor():
    print("Button A pressed, go!")
    motor.throttle = 1.0  # full speed!


def stop_motor():
    print("Button B pressed, stop!")
    motor.throttle = 0    # stop!


while True:
    if button_a.value:
    	start_motor()

    if button_b.value:
    	stop_motor()
