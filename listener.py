import asyncio

import websockets

from event import Event, EventType, MessageEvent


async def listen(uri, topic):
    async with websockets.connect(uri) as websocket:
        event = Event(EventType.SUBSCRIBE, topic)
        await websocket.send(event.to_json())

        while True:
            response = await websocket.recv()
            print("----------------------")
            print(f"Received response: {response}")
            print("----------------------")

            try:
                response_event = MessageEvent.from_json(response)
                print(f"Received response: {response_event.message}")
            except Exception as e:
                print(f"Failed to parse response: {response}.\nError: {e}")


if __name__ == "__main__":
    uri = "ws://localhost:8765"

    # Example usage
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            listen(uri, "topic1"),  # Client subscribing to "topic1"
        )
    )
