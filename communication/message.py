from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Union, Any

ValueT = TypeVar('ValueT', int, float)  # Must be int or float

BasicT = TypeVar('BasicT', int, float, str)  # for primitive type


@dataclass
class IMessage(ABC):
    pass


@dataclass
class BasicMessage(IMessage):
    data: BasicT


@dataclass
class VelocityMessage(IMessage):
    x: ValueT
    y: ValueT
    z: ValueT


@dataclass
class AngularVelocityMessage(IMessage):
    x: ValueT
    y: ValueT
    z: ValueT
