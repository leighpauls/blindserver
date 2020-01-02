import paho.mqtt.client as mqtt
import json

def handle_message(_client, _userdata, message):
    print(f'received message: {json.loads(message.payload)}')

def send_blinds_message(should_open: bool):
    client = mqtt.Client('command_server')
    client.connect('localhost')
    message_info = client.publish('/blinds', payload=json.dumps({'should_open': should_open}), qos=0)
    message_info.wait_for_publish()

if __name__ == '__main__':
    client = mqtt.Client('test_listener')
    client.connect('localhost')

    client.subscribe('/blinds')
    client.on_message = handle_message
    # client.publish('/blinds', payload=json.dumps({'openPercent': 100}), qos=0)

    for i in range(0, 30):
        client.loop()

if __name__ == '__main__' and False:
    send_blinds_message(True)
