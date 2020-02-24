import asyncio
import gpiozero
from typing import Optional
import time

import protocol

command_position: Optional[str] = None
command_expires_time: Optional[float] = None

COMMAND_EXPIRES_SECONDS = 5.0

async def on_connected(reader, writer):
    data = await reader.read(128)
    writer.close()
    if data not in protocol.COMMANDS:
        print("unknown command received")
        return
    print(f'recieved {data} command')
    global command_position
    global command_expires_time
    command_position = data
    command_expires_time = time.monotonic() + COMMAND_EXPIRES_SECONDS

async def control_loop():
    up_sensor = gpiozero.Button(2)
    down_sensor = gpiozero.Button(3)
    global command_position
    global command_expires_time

    while True:
        await asyncio.sleep(0.05)
        if (command_expires_time and time.monotonic() > command_expires_time) \
           or (command_position == protocol.OPEN_CMD and up_sensor.is_pressed) \
           or (command_position == protocol.CLOSE_CMD and down_sensor.is_pressed):
            command_expires_time = None
            command_position = None
        output_up = command_position == protocol.OPEN_CMD
        output_down = command_position == protocol.CLOSE_CMD
        print(f'desired_pos: {command_position},'
              f' up_sensor: {up_sensor.is_pressed},'
              f' down_sensor: {down_sensor.is_pressed},'
              f' output: u:{output_up} d:{output_down}')

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
