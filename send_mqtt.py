#!/usr/bin/python3

import paho.mqtt.client as mqtt
from get_temperature import get_data, print_data
import time
import json
import os
import requests

sensorId = '65b0cb7bd1f0bd05e47fa1f2'


def update_sensor(active):
    sensor = requests.get('http://10.0.0.76:8080/api/sensors/' + sensorId).json()
    sensor['active'] = active
    requests.put('http://10.0.0.76:8080/api/sensors/' + sensorId, json=sensor)


def get_client():
    client = mqtt.Client()
    if 'MQTT_USERNAME' in os.environ:
        client.username_pw_set(os.environ['MQTT_USERNAME'], os.environ['MQTT_PASSWORD'])
    client.connect('broker.emqx.io')
    return client


def loop(client):
    while True:
        data = get_data()
        data['sensor'] = sensorId
        print_data(data)
        client.publish('raspberry/mqtt', json.dumps(data))
        time.sleep(1)


if __name__ == "__main__":
    try:
        update_sensor(True)
        client = get_client()
        client.loop_start()
        loop(client)
    except KeyboardInterrupt:
        update_sensor(False)