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
    print('connecting...')
    client.connect('blinds-mqtt.leighpauls.com')
    print('connected')

    client.subscribe('/blinds')
    client.on_message = handle_message

    open_command = gpiozero.LED(23)
    close_command = gpiozero.LED(24)

    open_command.on()
    close_command.on()

    while True:
        if client.loop() != mqtt.MQTT_ERR_SUCCESS:
            print('lost connection')
            exit()

        if was_open != desired_open:
            print(f'change open from {was_open} to {desired_open}')
            was_open = desired_open
            if desired_open:
                close_command.off()
            else:
                open_command.off()

            time.sleep(1)
            open_command.on()
            close_command.on()

