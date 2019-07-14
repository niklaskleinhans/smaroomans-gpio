from threads.stopableThread import StopableThread
import paho.mqtt.client as mqtt
import json
import time
import datetime

class Subscriber():
    def __init__(self, host, states):
        self.host = host
        self.client = mqtt.Client('smaaroomansgpiomqttsubscriber')
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(self.host)
 
        self.states = states

    def on_message_from_notificationrgbled(self, client, userdata, message):
        topic = message.topic
        message = json.loads(message.payload.decode())
        print("subscribe: ", topic, message)
        try:
            room = message["room"]
            rgb = message["state"]
            for index, pin in enumerate(rgb):
                self.states[room]["notificationrgbled"][index].value = pin
        except Exception as e:
            print(e)

    def on_message_from_stateled(self, client, userdata, message):
        topic = message.topic
        message = json.loads(message.payload.decode())
        print("subscribe: ", topic, message)
        try:
            room = message["room"]
            state = message["state"]
            # states = message["data"]
            self.states[room]["stateled"].value = state
        except Exception as e:
            print(e)

    def on_connect(self, client, userdata, flags, rc):
        print("Subscriber Connected With Result Code ", rc)

    def on_disconnect(self, client, userdata, rc):
        print("Subscriber Client Got Disconnected")

    def subscribe(self, stopfunction=None):
        self.client.subscribe("actuator/notificationrgbled")
        self.client.subscribe("actuator/stateled")

        self.client.message_callback_add("actuator/notificationrgbled", self.on_message_from_notificationrgbled)
        self.client.message_callback_add("actuator/stateled", self.on_message_from_stateled)

        self.client.loop_start()

        # while(not stopfunction()):
            # print("client loop reconnect")
            # self.client.reconnect()
            # self.client.reconnect_delay_set(10)

    def startSubscription(self):
        self.subscribe()
        # self.subscriptionThread = StopableThread(name="subscriptionThread", function=self.subscribe, args={})
        # self.subscriptionThread.start()
        # while True:
        #     print(self.subscriptionThread.isAlive())
        #     print(datetime.datetime.now().timestamp())
        #     time.sleep(1)

    def stopSubscription(self):
        self.client.loop_stop()
        # self.subscriptionThread.stop()
    