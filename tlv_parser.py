from dataclasses import dataclass
from enum import IntEnum
from functools import partial
from typing import Any, List, Optional, Callable, TypeVar, Tuple, Iterable


class Type(IntEnum):
    BOOL = 1
    STRING = 2


@dataclass
class Data:
    type: Type
    value: Any


def bitstring_to_bytes(s: str) -> bytes:
    """ :raises OverflowError: if len(s) is not a multiple of 8 """
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')


class DecodeError(Exception):
    pass


def decode_data(bytes_stream: bytes, data_type: Type):
    """ :raises NotImplementedError: TODO delete"""

    data = Data(data_type, None)
    if data_type == Type.BOOL:
        data.value = True if len(bytes_stream) == 1 and bytes_stream[0] & 0xFF else False
    elif data_type == Type.STRING:
        pass
    else:
        raise NotImplementedError("Type is not implemented")

    return data


def decode_tlv(bytes_stream: bytes):
    """ :param bytes_stream: list of 8 """

    i = 0

    classification_byte = bytes_stream[i]

    class_2bit = classification_byte >> 6
    form = classification_byte & 1 << 5
    type_number = classification_byte & 0b1111

    if type_number > 30:
        i += 1
        if bytes_stream[i] & 128 == 0:
            type_number = bytes_stream[i] & 127
        else:
            type_number = 0
            while True:
                type_number <<= 8
                type_number |= bytes_stream[i] & 127
                if bytes_stream[i] & 128 == 0:
                    break
                i += 1

    # TODO - add different class of types and constructed
    data_type = Type(type_number)

    i += 1
    length = bytes_stream[i]
    if length & 128 != 0:
        n = length & 127
        length = 0
        for _ in range(n):
            i += 1
            length <<= 8
            length |= bytes_stream[i]

    i += 1
    data = decode_data(bytes_stream[i: i+length], data_type)

    return data

###############################
# functional approach -> mess, TODO - delete

T = TypeVar('T')
R = TypeVar('R')
parser_result_t = Optional[Tuple[T, List[T]]]
parser_t = Callable[[T], parser_result_t]


def match_input(parser_input: List[T], c: T) -> parser_result_t:
    return (c, parser_input[len(c):]) if parser_input[:len(c)] == c else None


def one_of(cs: Iterable[T]) -> parser_t:
    def one_of_parser(parser_intput: List[T]):
        for c in cs:
            if parser_intput[:len(c)] == c:
                return c, parser_intput[len(c):]
        return None
    return one_of_parser


def none_of(cs: Iterable[T]) -> parser_t:
    def none_of_parser(parser_intput: List[T]):
        for c in cs:
            if parser_intput[:len(c)] == c:
                return None
        return parser_intput[:len(cs[0])], parser_intput[len(cs[0]):]
    return none_of_parser


def make_match_input(c: T) -> parser_t:
    return partial(match_input, c=c)


def fmap(parser: parser_t, f: Callable[[T], R]) -> Callable[[T], Optional[Tuple[R, List[R]]]]:
    return lambda parser_input: (
        f((x := parser(parser_input))[0]),
        f(x[1])
    )


def alternate(parser_1: parser_t, parser_2: parser_t) -> parser_t:
    return lambda parser_input: x if (x := parser_1(parser_input)) else parser_2(parser_input)


def combine(parser_1: parser_t, parser_2: parser_t, join: Callable[[T, T], T]) -> parser_t:
    return lambda parser_input: \
        (join(x[0], y[0]),  y[1]) if (x := parser_1(parser_input)) and (y := parser_2(x[1])) else None


def many(parser: parser_t, b: T, join: Callable[[T, T], T]) -> parser_t:
    def many_parser(parser_input):
        remaining_input = parser_input
        accumulation = b
        while remaining_input:
            r = parser(remaining_input)
            if r is None:
                return accumulation, remaining_input
            accumulation = join(accumulation, r[0])
            remaining_input = r[1]
    return many_parser

# def exactly_n(parser: parser_t, n: int) -> parser_result_t:
#     return lambda parser_input: [ for ]

###############################


# Some basic functionality test
if __name__ == '__main__':
    tag = bitstring_to_bytes('00 0 00001'.replace(' ', ''))
    length = bitstring_to_bytes('0 0000001'.replace(' ', ''))
    data = 0xFF.to_bytes(1, 'big')

    byte_stream = bytes()
    byte_stream += tag + length + data
    print(byte_stream)

    data_lst = decode_tlv(byte_stream)


