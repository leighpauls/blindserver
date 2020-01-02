import paho.mqtt.client as mqtt
import json
import gpiozero
import time

was_open = None
desired_open = None


def handle_message(_client, _userdata, message):
    json_payload = json.loads(message.payload)
    print(f'received message: {json_payload}')
    global desired_open
    desired_open = json_payload['should_open']

if __name__ == '__main__':
    client = mqtt.Client('pi_listener')
    client.connect('blinds-mqtt.leighpauls.com')

    client.subscribe('/blinds')
    client.on_message = handle_message

    open_command = gpiozero.LED(23)
    close_command = gpiozero.LED(24)

    while True:
        client.loop()
        if was_open != desired_open:
            print(f'change open from {was_open} to {desired_open}')
            was_open = desired_open
            if desired_open:
                open_command.on()
            else:
                close_command.on()

            time.sleep(1)
            open_command.off()
            close_command.off()

