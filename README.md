# WebSocket Chat Application

This is a simple WebSocket chat application written in Python.
The application includes a server and two client executables.

* The server allows clients to connect, subscribe to topics, and send messages to those topics.
* The listener client listens to messages on a specific topic.
* The sender client sends messages to a specific topic.

## Requirements

- Python 3.7+
- `websockets` library

You can install the required library using pip:

```bash
pip install websockets
```

## Executables

### `sender.py`

This script connects to the WebSocket server and sends messages to a specified topic.

## Usage

### Running the WebSocket Server

To start the WebSocket server, run:

```bash
python3 server.py
```

This script runs the WebSocket server that manages client connections, subscriptions to topics, and message
broadcasting.
The server will start and listen for client connections on `ws://localhost:8765

### Listening to a Topic

To listen to messages on a specific topic, use the `listener.py` script.
You need to specify the topic you want to listen to as an argument:

```bash
python3 listener.py <topic_name>
```

For example, to listen to messages on the topic "topic1":

```bash
python3 listener.py topic1
```

### Sending Messages to a Topic

To send messages to a specific topic, use the `sender.py` script.
You need to specify the topic as arguments:

```bash
python3 sender.py <topic_name>
```