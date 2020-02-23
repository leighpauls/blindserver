import paho.mqtt.client as mqtt
import json
import time
import socket

import protocol

def handle_message(_client, _userdata, message):
    json_payload = json.loads(message.payload)
    print(f'received message: {json_payload}')
    desired_open = json_payload['should_open']

    command_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    command_socket.connect(protocol.ADDRESS)
    command_socket.sendall(protocol.OPEN_CMD if desired_open else protocol.CLOSE_CMD)
    command_socket.close()

if __name__ == '__main__':
    client = mqtt.Client('pi_listener_client')

    while True:
        print('connecting...')
        client.connect('blinds-mqtt.leighpauls.com')
        print('connected')

        client.subscribe('/blinds')
        client.on_message = handle_message

        while client.loop() == mqtt.MQTT_ERR_SUCCESS:
            pass
