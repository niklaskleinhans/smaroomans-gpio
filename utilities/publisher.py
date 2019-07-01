from threads.stopableThread import StopableThread
import paho.mqtt.client as mqtt
import json
import time

class Publisher():
    def __init__(self, host):
        self.host = host
        self.client = mqtt.Client('smaaroomansgpiomqttpublisher')
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(self.host)

    def on_connect(self, client, userdata, flags, rc):
        print("Publisher Connected With Result Code ", rc)

    def on_disconnect(self, client, userdata, rc):
        print("Publisher Client Got Disconnected")
        self.client.connect(self.host)

    def publish(self, topic, data):
        self.client.publish(topic, json.dumps(data))
        # self.client.reconnect_delay_set(10)
