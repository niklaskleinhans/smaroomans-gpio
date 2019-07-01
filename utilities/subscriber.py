from threads.stopableThread import StopableThread
import paho.mqtt.client as mqtt
import json
import time
import datetime

class Subscriber():
    # def __init__(self, host, statusRGBLED, statusRooms):
    def __init__(self, host, states):
        self.host = host
        self.client = mqtt.Client('smaaroomansgpiomqttsubscriber')
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(self.host)
        # self.statusRGBLED = statusRGBLED
        # self.statusRooms = statusRooms
        self.states = states

    def on_message_from_notificationrgbled(self, client, userdata, message):
        message = json.loads(message.payload.decode())
        try:
            room = message["room"]
            rgb = message["state"]
            for index, pin in enumerate(rgb):
                self.states[room]["notificationrgbled"][index].value = pin
        except Exception as e:
            print(e)

    # def on_message_from_statusRGBLED(self, client, userdata, message):
    #     message = json.loads(message.payload.decode())
    #     try:
    #         rgb = message["state"]
    #         for index, pin in enumerate(rgb):
    #             self.statusRGBLED[index].value = pin
    #     except Exception as e:
    #         print(e)

    def on_message_from_stateled(self, client, userdata, message):
        message = json.loads(message.payload.decode())
        try:
            room = message["room"]
            state = message["state"]
            # states = message["data"]
            self.states[room]["stateled"].value = state
        except Exception as e:
            print(e)

    # def on_message_from_statusRooms(self, client, userdata, message):
    #     message = json.loads(message.payload.decode())
    #     try:
    #         states = message["data"]
    #         for index, pin in enumerate(states):
    #             self.statusRooms[index].value = pin
    #     except Exception as e:
    #         print(e)

    def on_connect(self, client, userdata, flags, rc):
        print("Subscriber Connected With Result Code ", rc)

    def on_disconnect(self, client, userdata, rc):
        print("Subscriber Client Got Disconnected")

    def subscribe(self, stopfunction=None):
        self.client.subscribe("actuator/notificationrgbled")
        self.client.subscribe("actuator/stateled")

        self.client.message_callback_add("actuator/notificationrgbled", self.on_message_from_notificationrgbled)
        self.client.message_callback_add("actuator/stateled", self.on_message_from_stateled)

        while(not stopfunction()):
            self.client.loop()
            # print("client loop reconnect")
            # self.client.reconnect()
            # self.client.reconnect_delay_set(10)

    def startSubscription(self):
        # self.subscribe()
        self.subscriptionThread = StopableThread(name="subscriptionThread", function=self.subscribe, args={})
        self.subscriptionThread.start()
        # while True:
        #     print(self.subscriptionThread.isAlive())
        #     print(datetime.datetime.now().timestamp())
        #     time.sleep(1)

    def stopSubscription(self):
        self.subscriptionThread.stop()
    