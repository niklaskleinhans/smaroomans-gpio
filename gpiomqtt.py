from utilities.subscriber import Subscriber
from utilities.publisher import Publisher

from gpiozero import LED, Button
from time import sleep
from signal import pause

import os
import sys

import json
import paho.mqtt.client as mqtt

class GpioMqtt():

    def __init__(self):
        self.windowButton = Button(18)
        # self.statusRGBLED = [LED(22), LED(27), LED(17)]
        # self.statusRoomLEDs = [LED(26), LED(19), LED(13), LED(6), LED(5), LED(21), LED(20), LED(16), LED(12), LED(25)]
        self.states = {"room1": {"stateled": LED(26), "notificationrgbled": [LED(22), LED(27), LED(17)]}, 
                      "room2": {"stateled": LED(19)}, "room3": {"stateled": LED(13)}, "room4": {"stateled": LED(6)},
                      "room5": {"stateled": LED(5)}, "room6": {"stateled": LED(21)}, "room7": {"stateled": LED(20)},
                      "room8": {"stateled": LED(16)}, "room9": {"stateled": LED(12)}, "room10": {"stateled": LED(25)}}
        self.subscriber = Subscriber("192.168.1.230", self.states)
        self.publisher = Publisher("192.168.1.230")

    def windowClosed(self):
        self.publisher.publish("gpio/sensor/window", {"window": 0})

    def windowOpened(self):
        self.publisher.publish("gpio/sensor/window", {"window": 1})

    def checkWindow(self):
        self.windowButton.when_pressed = self.windowClosed
        self.windowButton.when_released = self.windowOpened

        pause()

    def startSubscription(self):
        self.subscriber.startSubscription()

    def stopSubscription(self):
        self.subscriber.stopSubscription()

    def startPublisher(self):
        self.publisher.startPublisher()

    def stopPublisher(self):
        self.publisher.stopPublisher()

def main():
    gpiomqtt = GpioMqtt()
    gpiomqtt.startSubscription()
    gpiomqtt.startPublisher()
    gpiomqtt.checkWindow()

if __name__ == "__main__":
    main()

