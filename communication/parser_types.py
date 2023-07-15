from dataclasses import dataclass
from enum import IntEnum
from typing import Union


class TagType(IntEnum):
    UNIVERSAL = 0
    APPLICATION = 1
    CONTEXT_SPECIFIC = 2
    PRIVATE = 3


class TagForm(IntEnum):
    PRIMITIVE = 0
    CONSTRUCTED = 1


@dataclass
class Tag:
    type: Union[TagType, int]   # classification
    form: Union[TagForm, int]
    number: int


@dataclass
class ByteData:
    tag: Tag
    value: Union[bytes, 'ByteData']

