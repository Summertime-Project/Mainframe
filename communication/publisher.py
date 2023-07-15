import weakref
from typing import Callable, Set

from communication.message import IMessage

UpdateFunctionT = Callable[[IMessage], None]


class Publisher:
    """ Sends ALL messages to ALL callbacks """
    def __init__(self):
        self.callbacks: Set[weakref.WeakMethod[UpdateFunctionT]] = set()

    def add_callback(self, callback: UpdateFunctionT):
        self.callbacks.add(weakref.WeakMethod(callback))

    def delete_callback(self, callback: UpdateFunctionT):
        self.callbacks.remove(weakref.WeakMethod(callback))

    def has(self, callback: UpdateFunctionT) -> bool:
        return weakref.WeakMethod(callback) in self.callbacks

    def update_callback(self, message):
        for callback in self.callbacks:
            if (x := callback()) is not None:
                x(message)
