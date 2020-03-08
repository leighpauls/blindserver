import asyncio
import gpiozero
from typing import Optional
import time

import protocol


class BlindIO:
    up_sensor: gpiozero.Button
    down_sensor: gpiozero.Button
    up_motor: gpiozero.LED
    down_motor: gpiozero.LED

    def __init__(self, up_sensor: int, down_sensor: int, up_motor: int, down_motor: int):
        self.up_sensor = gpiozero.Button(up_sensor)
        self.down_sensor = gpiozero.Button(down_sensor)
        self.up_motor = gpiozero.LED(up_motor)
        self.down_motor = gpiozero.LED(down_motor)


class BlindController:
    io: BlindIO
    command_position: Optional[bytes] = None
    command_expires_time: Optional[float] = None

    def __init__(self, io: BlindIO):
        self.io = io
        self.command_position = None
        self.command_expires_time = None

    def control_step(self, cur_time: float):
        # Check if the command is completed or expired
        if (self.command_expires_time and cur_time > self.command_expires_time) \
           or (self.command_position == protocol.OPEN_CMD and self.io.up_sensor.is_pressed) \
           or (self.command_position == protocol.CLOSE_CMD and self.io.down_sensor.is_pressed):
            self.command_expires_time = None
            self.command_position = None

        self.io.up_motor.value = self.command_position == protocol.OPEN_CMD
        self.io.down_motor.value = self.command_position == protocol.CLOSE_CMD


blinds = [
    BlindController(BlindIO(2, 3, 17, 27))
]

COMMAND_EXPIRES_SECONDS = 5.0

async def on_connected(reader, writer):
    data = await reader.read(128)
    writer.close()
    if data not in protocol.COMMANDS:
        print("unknown command received")
        return
    print(f'recieved {data} network command')
    set_command(data, time.monotonic())

def set_command(new_position: bytes, cur_time: float):
    global blinds
    for b in blinds:
        b.command_position = new_position
        b.command_expires_time = cur_time + COMMAND_EXPIRES_SECONDS

async def control_loop() -> None:
    up_command_button = gpiozero.Button(14)
    down_command_button = gpiozero.Button(15)

    global blinds

    while True:
        await asyncio.sleep(0.05)

        cur_time = time.monotonic()

        if up_command_button.is_pressed and not down_command_button.is_pressed:
            set_command(protocol.OPEN_CMD, cur_time)
        elif down_command_button.is_pressed and not up_command_button.is_pressed:
            set_command(protocol.CLOSE_CMD, cur_time)

        for b in blinds:
            b.control_step(cur_time)

def main() -> None:
    loop = asyncio.get_event_loop()
    print("starting server")
    command_server = loop.run_until_complete(
        asyncio.start_unix_server(on_connected, path=protocol.ADDRESS))
    print("started server")

    loop.create_task(control_loop())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("stopped for keyboard interrupt")
        pass
    finally:
        print("cleaning up")
        command_server.close()
        loop.run_until_complete(command_server.wait_closed())

if __name__ == '__main__':
    main()
