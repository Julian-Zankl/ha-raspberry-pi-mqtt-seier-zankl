#!/usr/bin/python3

import paho.mqtt.client as mqtt
from get_temperature import get_data, print_data
import time
import json
import os
import requests

def create_client():
    sensor = requests.post('http://10.0.0.76:8080/api/sensors', json={"name": "Snensor", "location": "Grafenschachen", "active": True, "type": "INDOOR"})
    return sensor.json()['id']


def get_client():
    client = mqtt.Client()
    if 'MQTT_USERNAME' in os.environ:
        client.username_pw_set(
            os.environ['MQTT_USERNAME'], os.environ['MQTT_PASSWORD'])
    client.connect('broker.emqx.io')
    return client


def loop(client, sensor):
    while True:
        data = get_data()
        data['sensor'] = sensor
        print_data(data)
        client.publish('raspberry/mqtt', json.dumps(data))
        time.sleep(1)


if __name__ == "__main__":
    sensor = create_client()
    client = get_client()
    client.loop_start()
    loop(client, sensor)