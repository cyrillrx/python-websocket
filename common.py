from event import MessageEvent


def handle_response(response:str):
    print("----------------------")
    print(f"Received response: {response}")
    print("----------------------")

    try:
        response_event = MessageEvent.from_json(response)
        print(f"Received response: {response_event.message}")
    except Exception as e:
        print(f"Failed to parse response: {response}.\nError: {e}")
