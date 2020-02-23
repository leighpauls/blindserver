import asyncio
import protocol

async def on_connected(reader, writer):
    data = await reader.read(128)
    writer.close()
    if data == protocol.OPEN_CMD:
        print("recieved open command")
    elif data == protocol.CLOSE_CMD:
        print("recieved close command")
    else:
        print("unknown command received")

def main() -> None:
    loop = asyncio.get_event_loop()
    print("starting server")
    command_server = loop.run_until_complete(asyncio.start_unix_server(on_connected, path=protocol.ADDRESS))
    print("started server")

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
