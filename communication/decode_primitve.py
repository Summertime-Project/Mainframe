from typing import Union
from enum import IntEnum


class DecodeError(Exception):
    pass


class PrimitiveType(IntEnum):
    BOOL = 1
    INT = 2
    STRING = 3
    REAL = 9


def decode_bool(byte: bytes) -> bool:
    if byte == b'\xFF':
        return True
    elif byte == b'\x00':
        return False
    raise DecodeError


def decode_int(byte: Union[bytes, int]) -> int:
    if type(byte) == int:
        return byte
    return int.from_bytes(byte, 'big')


def decode_string(byte: bytes) -> str:
    raise NotImplementedError()


def decode_real(byte: bytes) -> float:
    Mantissa_byte = byte[0]
    S = (Mantissa_byte & (1 << 6)) >> 6
    B = (Mantissa_byte & (0b11 << 4)) >> 4

    S = 1 if S == 0 else -1

    # unsure
    if B == 0:
        B = 2
    elif B == 1:
        B = 8
    elif B == 2:
        B = 10
    else:
        B = 16

    F = (Mantissa_byte & (0b11 << 2)) >> 2

    E = byte[1]
    N = decode_int(byte[2:])

    M = float(S * N * (2 ** F))
    return M * (B ** E)


if __name__ == '__main__':
    print(decode_int(b'\x48'))
