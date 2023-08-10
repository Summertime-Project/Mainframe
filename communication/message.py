from dataclasses import dataclass
from typing import TypeVar


""" Type of message """
MessageT = TypeVar("MessageT",
                   type(bool),
                   int,
                   str,
                   float,
                   'VelocityMessage',
                   'AngularVelocityMessage'
                   )

_ValueT = TypeVar('_ValueT', int, float)


@dataclass(eq=True, frozen=True)
class VelocityMessage:
    x: _ValueT
    y: _ValueT
    z: _ValueT


@dataclass(eq=True, frozen=True)
class AngularVelocityMessage:
    x: _ValueT
    y: _ValueT
    z: _ValueT
