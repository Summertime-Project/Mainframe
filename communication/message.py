from abc import ABC
from dataclasses import dataclass
from enum import IntEnum
from typing import TypeVar, Union


class PublicType(IntEnum):
    """ TLV public data types """
    BOOL = 1
    STRING = 2


class PrimitiveTypes(IntEnum):
    REQUEST = 0
    RFU = 1
    CO1 = 2


class ConstructedTypes(IntEnum):
    ALL = 0
    VELOCITY = 1
    ANGULAR_VELOCITY = 2
    POSITION = 3
    ANGLE = 4


ValueT = TypeVar('ValueT', int, float)  # Must be int or float


# bad design, too much coupling, TODO - redo
@dataclass
class IMessage(ABC):
    type: Union[ConstructedTypes, PrimitiveTypes]


@dataclass
class ConstructedMessage(IMessage):
    x: ValueT
    y: ValueT
    z: ValueT
