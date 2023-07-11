from typing import Callable, Set

from message import IMessage


class Publisher:
    """ Sends ALL messages to ALL callbacks"""
    UpdateFunctionT = Callable[[IMessage], None]
    _callbacks: Set[UpdateFunctionT] = set()

    def add_callback(self, callback: UpdateFunctionT):
        self._callbacks.add(callback)

    def delete_callback(self, callback: UpdateFunctionT):
        self._callbacks.discard(callback)

    def has_callback(self, callback: UpdateFunctionT) -> bool:
        return callback in self._callbacks

    def update_callbacks(self, message):
        """ Sends message to all callbacks """
        for callback in self._callbacks:
            callback(message)
