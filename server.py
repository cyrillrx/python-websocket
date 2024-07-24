import asyncio

import websockets

from event import EventType, Event, MessageEvent

# All connected subscribers. Key: websocket, Value: topic. 1 to 1 relationship.
subscribers = {}
# All topics and their subscribers. Key: topic, Value: set of websockets. 1 to n relationship.
topics = {}


async def handler(websocket):
    await register(websocket)
    try:
        async for message in websocket:
            print("----------------------")
            print(f"Received message: {message}")
            print("----------------------")

            try:
                event: Event = Event.from_json(message)
                await handle_event(websocket, event, message)
            except Exception as e:
                print(f"Failed to parse message: {message}.\nError: {e}")
                continue

    except Exception as e:
        print("----------------------")
        print(f"Error in handler: {e}")
        print("----------------------")
    finally:
        await unregister(websocket)


async def register(websocket):
    subscribers[websocket] = None


async def unregister(websocket):
    if websocket not in subscribers: return

    topic = subscribers[websocket]
    if topic in topics:
        topics[topic].remove(websocket)

    del subscribers[websocket]


async def handle_event(websocket, event: Event, original_message: str):
    match event.type:
        case EventType.SUBSCRIBE:
            await subscribe(websocket, event.topic)
        case EventType.UNSUBSCRIBE:
            await unsubscribe(websocket, event.topic)
        case EventType.PUBLISH:
            message_event = MessageEvent.from_json(original_message)
            await publish(websocket, message_event)


async def subscribe(websocket, topic: str):
    try:
        if topic not in topics:
            topics[topic] = set()

        topics[topic].add(websocket)
        subscribers[websocket] = topic

        event = MessageEvent(topic, f"Subscribed to topic {topic}")
        await websocket.send(event.to_json())
    except Exception as e:
        print(f"An error occurred while subscribing to topic: {topic}.\nError: {e}")


async def unsubscribe(websocket, topic: str):
    try:
        if topic in topics:
            topics[topic].remove(websocket)
            subscribers[websocket] = None

        event = MessageEvent(topic, f"Unsubscribed from topic {topic}")
        await websocket.send(event.to_json())
    except Exception as e:
        print(f"An error occurred while unsubscribing to topic: {topic}.\nError: {e}")


async def publish(current_ws_client, event: MessageEvent):
    try:
        topic = event.topic

        if topic not in topics: return  # No subscribers to this topic

        event_str = event.to_json()
        for client in topics[topic]:
            if client != current_ws_client:
                await client.send(event_str)

        response = MessageEvent(topic, f"Message sent to topic {topic}")
        await current_ws_client.send(response.to_json())
    except Exception as e:
        print(f"An error occurred while publish event: {event.to_json()}.\nError: {e}")


start_server = websockets.serve(handler, "localhost", 8765)

print("Ready to listen on ws://localhost:8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
