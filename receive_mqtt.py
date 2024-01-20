#!/usr/bin/python3

from send_mqtt import get_client
import json
import requests

device = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("raspberry/mqtt")

def on_message(client, userdata, message):
    data = json.loads(message.payload)
    print(data)
    requests.post('http://10.0.0.76:8080/api/measurements', json=data)
    

if __name__ == "__main__":
    client = get_client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()