import asyncio

import websockets

from common import handle_response
from event import EventType, Event, MessageEvent


async def send(uri, topic, message):
    async with websockets.connect(uri) as websocket:
        event = MessageEvent(topic, message)
        await websocket.send(event.to_json())

        response = await websocket.recv()
        handle_response(response)


if __name__ == "__main__":
    uri = "ws://localhost:8765"

    # Example usage
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            send(uri, "topic1", "Hello, Topic1!")  # Client sending message to "topic1"
        )
    )
