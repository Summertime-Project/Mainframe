from typing import Callable, Dict, List, Type
from weakref import WeakMethod

from communication.message import MessageT

CallbackT = Callable[[MessageT], None]


class Publisher:
    """
        Maps type of message to callbacks
        Holds a weak reference to prevent memory leaks
    """
    def __init__(self):
        self.callbacks: Dict[Type[MessageT], List[WeakMethod[CallbackT]]] = {}

    def add_callback(self, message_type: Type[MessageT], callback: CallbackT):
        if message_type not in self.callbacks.keys():
            self.callbacks[message_type] = []
        self.callbacks[message_type].append(WeakMethod(callback))

    def remove_callback(self, message_type: Type[MessageT], callback: CallbackT):
        try:
            self.callbacks[message_type].remove(WeakMethod(callback))
        except KeyError or ValueError:
            return

    def has(self, message_type: Type[MessageT], callback: CallbackT) -> bool:
        if message_type in self.callbacks.keys():
            return WeakMethod(callback) in self.callbacks[message_type]
        return False

    def update_callback(self, message: MessageT):
        message_type = type(message)
        if message_type not in self.callbacks.keys():
            return
        for callback in self.callbacks[message_type]:
            if (x := callback()) is not None:
                x(message)
