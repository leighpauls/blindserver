import paho.mqtt.client as mqtt
import json

def handle_message(_client, _userdata, message):
    print(f'received message: {json.loads(message.payload)}')

if __name__ == '__main__':
    client = mqtt.Client('pi_listener')
    client.connect('blinds-mqtt.leighpauls.com')

    client.subscribe('/blinds')
    client.on_message = handle_message

    while True:
        client.loop()

