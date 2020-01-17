#!/usr/bin/env python
""" Main bot module to be compiled down to MicroPython """

from digitalio import DigitalInOut, Pull, Direction
import board
from adafruit_crickit import crickit

# Two onboard CPX buttons for input (low level saves memory)
BUTTON_A = DigitalInOut(board.BUTTON_A)
BUTTON_A.direction = Direction.INPUT
BUTTON_A.pull = Pull.DOWN

BUTTON_B = DigitalInOut(board.BUTTON_B)
BUTTON_B.direction = Direction.INPUT
BUTTON_B.pull = Pull.DOWN

""" Create one motor on seesaw motor port #1 """
MOTOR = crickit.dc_motor_1

def start_motor():
    """ Helper function to start motor """
    print("Button A pressed, go!")
    MOTOR.throttle = 1.0  # full speed!

def stop_motor():
    """ Helper function to stop motor """
    print("Button B pressed, stop!")
    MOTOR.throttle = 0    # stop!


while True:
    if BUTTON_A.value:
        start_motor()
    elif BUTTON_B.value:
        stop_motor()
