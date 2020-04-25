#!/usr/bin/env python
""" Main bot module to be compiled down to MicroPython """

# Circuit Playground Bluefruit Rover
# Use with the Adafruit BlueFruit LE Connect app
# Works with CircuitPython 5.0.0-beta.0 and later
# running on an nRF52840 CPB board and Crickit

import time
import board
import digitalio
import neopixel
from adafruit_crickit import crickit

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket

# Prep the status LED on the CPB
RED_LED = digitalio.DigitalInOut(board.D13)
RED_LED.direction = digitalio.Direction.OUTPUT

BLE = BLERadio()
UART_SERVICE = UARTService()
ADVERTISEMENT = ProvideServicesAdvertisement(UART_SERVICE)

# motor setup
MOTOR_ONE = crickit.dc_motor_1
MOTOR_TWO = crickit.dc_motor_2

FWD = 1.0
REV = -1.0

NEOPIXELS = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
PURPLE = (120, 0, 160)
YELLOW = (100, 100, 0)
AQUA = (0, 100, 100)
BLACK = (0, 0, 0)
COLOR = PURPLE  # current NeoPixel color
NEOPIXELS.fill(COLOR)

print("BLE Turtle Rover")
print("Use Adafruit Bluefruit app to connect")
while True:
    NEOPIXELS[0] = BLACK
    NEOPIXELS.show()
    BLE.start_advertising(ADVERTISEMENT)
    while not BLE.connected:
        # Wait for a connection.
        pass
    # set a pixel blue when connected
    NEOPIXELS[0] = BLUE
    NEOPIXELS.show()
    while BLE.connected:
        if UART_SERVICE.in_waiting:
            # Packet is arriving.
            RED_LED.value = False  # turn off red LED
            PACKET = Packet.from_stream(UART_SERVICE)
            if isinstance(PACKET, ColorPacket):
                # Change the COLOR.
                COLOR = PACKET.color
                NEOPIXELS.fill(COLOR)

            # do this when buttons are pressed
            if isinstance(PACKET, ButtonPacket) and PACKET.pressed:
                RED_LED.value = True  # blink to show packet has been received
                if PACKET.button == ButtonPacket.UP:
                    NEOPIXELS.fill(COLOR)
                    MOTOR_ONE.throttle = FWD
                    MOTOR_TWO.throttle = FWD
                elif PACKET.button == ButtonPacket.DOWN:
                    NEOPIXELS.fill(COLOR)
                    MOTOR_ONE.throttle = REV
                    MOTOR_TWO.throttle = REV
                elif PACKET.button == ButtonPacket.RIGHT:
                    COLOR = YELLOW
                    NEOPIXELS.fill(COLOR)
                    MOTOR_TWO.throttle = 0
                    MOTOR_ONE.throttle = FWD
                elif PACKET.button == ButtonPacket.LEFT:
                    COLOR = YELLOW
                    NEOPIXELS.fill(COLOR)
                    MOTOR_TWO.throttle = FWD
                    MOTOR_ONE.throttle = 0
                elif PACKET.button == ButtonPacket.BUTTON_1:
                    NEOPIXELS.fill(RED)
                    MOTOR_ONE.throttle = 0.0
                    MOTOR_TWO.throttle = 0.0
                    time.sleep(0.5)
                    NEOPIXELS.fill(COLOR)
                elif PACKET.button == ButtonPacket.BUTTON_2:
                    COLOR = GREEN
                    NEOPIXELS.fill(COLOR)
                elif PACKET.button == ButtonPacket.BUTTON_3:
                    COLOR = BLUE
                    NEOPIXELS.fill(COLOR)
                elif PACKET.button == ButtonPacket.BUTTON_4:
                    COLOR = PURPLE
                    NEOPIXELS.fill(COLOR)
            # do this when some buttons are released
            elif isinstance(PACKET, ButtonPacket) and not PACKET.pressed:
                if PACKET.button == ButtonPacket.UP:
                    NEOPIXELS.fill(RED)
                    MOTOR_ONE.throttle = 0
                    MOTOR_TWO.throttle = 0
                if PACKET.button == ButtonPacket.DOWN:
                    NEOPIXELS.fill(RED)
                    MOTOR_ONE.throttle = 0
                    MOTOR_TWO.throttle = 0
                if PACKET.button == ButtonPacket.RIGHT:
                    NEOPIXELS.fill(RED)
                    MOTOR_ONE.throttle = 0
                    MOTOR_TWO.throttle = 0
                if PACKET.button == ButtonPacket.LEFT:
                    NEOPIXELS.fill(RED)
                    MOTOR_ONE.throttle = 0
                    MOTOR_TWO.throttle = 0
