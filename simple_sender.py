import argparse
import asyncio

import websockets


def main():
    parser = argparse.ArgumentParser(description="Send message to ws://localhost:8765.")
    parser.add_argument("message", type=str, help="Message to send")
    args = parser.parse_args()

    uri = "ws://localhost:8765"

    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            send(uri, args.message)
        )
    )


async def send(uri, message):
    async with websockets.connect(uri) as websocket:
        print("----------------------")
        print("----------------------")
        print(f"Sending message: {message}")
        await websocket.send(message)

        while True:
            response = await websocket.recv()
            print(f"Received response: {response}")
            if response == "bye":
                websocket.close(CloseReason.NORMAL_CLOSURE, reason="Server said bye")
                break


if __name__ == "__main__":
    main()
