import asyncio

import websockets

from common import handle_response
from event import EventType, Event


async def listen(uri, topic):
    async with websockets.connect(uri) as websocket:
        event = Event(EventType.SUBSCRIBE, topic)
        await websocket.send(event.to_json())

        while True:
            response = await websocket.recv()
            handle_response(response)


if __name__ == "__main__":
    uri = "ws://localhost:8765"

    # Example usage
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            listen(uri, "topic1"),  # Client subscribing to "topic1"
        )
    )
