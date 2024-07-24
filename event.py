import json
from enum import Enum


class EventType(Enum):
    SUBSCRIBE = 1
    UNSUBSCRIBE = 2
    PUBLISH = 3


class Event:
    def __init__(self, type: EventType, topic: str):
        self.type = type
        self.topic = topic

    def to_json(self):
        return json.dumps({
            "type": self.type.value,
            "topic": self.topic
        })

    @staticmethod
    def from_json(data_str: str) -> 'Event':
        data_dict = json.loads(data_str)
        return Event(
            type=EventType(data_dict.get("type")),
            topic=data_dict.get("topic")
        )


class MessageEvent(Event):
    def __init__(self, topic: str, message: str):
        super().__init__(type=EventType.PUBLISH, topic=topic)
        self.message = message

    def to_json(self):
        return json.dumps({
            "type": self.type.value,
            "topic": self.topic,
            "message": self.message,
        })

    @staticmethod
    def from_json(data_str: str) -> 'MessageEvent':
        data_dict = json.loads(data_str)
        return MessageEvent(
            topic=data_dict.get("topic"),
            message=data_dict.get("message"),
        )
