from dataclasses import dataclass
from typing import Any, Union, Type

import crc8
from message import IMessage, PrimitiveTypes, ConstructedTypes


class DecodeError(Exception):
    pass


class BadFrameError(Exception):
    pass


@dataclass
class Data:
    """ For parser implementation """
    type: Union[PrimitiveTypes, ConstructedTypes]
    value: Any


def bitstring_to_bytes(s: str) -> bytes:
    """ :raises OverflowError: if len(s) is not a multiple of 8 """
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')


def decode_data(bytes_stream: bytes, data_type: Union[PrimitiveTypes, ConstructedTypes]):
    """ Interprets a bytes to correct data type
        :raises NotImplementedError: for not implemented data types
    """
    data = Data(data_type, None)

    if data_type == ConstructedTypes.ALL:
        raise NotImplementedError("Type is not implemented")

    elif data_type == ConstructedTypes.VELOCITY:
        raise NotImplementedError("Type is not implemented")

    elif data_type == ConstructedTypes.ANGULAR_VELOCITY:
        raise NotImplementedError("Type is not implemented")

    elif data_type == ConstructedTypes.POSITION:
        raise NotImplementedError("Type is not implemented")

    elif data_type == ConstructedTypes.ANGLE:
        raise NotImplementedError("Type is not implemented")

    else:
        raise NotImplementedError("Type is not implemented")

    return data


def decode_tlv(bytes_stream: bytes) -> Data:
    """
        Splits a single tlv frame to type and bytes of data
        HANDLES ONLY PRIVATE TAGS

        :param bytes_stream: list of 8 bits
        :return: data corresponding to the received frame
    """
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

    if form == 0:  # primitive
        data_type = PrimitiveTypes(type_number)
    else:
        data_type = ConstructedTypes(type_number)

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


# TODO - complete
def decode(bytes_stream: bytes) -> Type[IMessage]:
    """
        Decodes a big encapsulation frame
        :param bytes_stream: list of 8 bits
        :raises BadFrameError: mismatch between CRC8
    """
    conf_byte = bytes_stream[0]
    data_length = bytes_stream[1]
    tlv_data = bytes_stream[2:-1]
    crc_8bit = bytes_stream[-1]

    # Checking CRC, TODO - check is CONF in CRC ??
    crc8_hash = crc8.crc8()
    crc8_hash.update(bytes_stream[:-1])

    calculated_crc8 = int.from_bytes(crc8_hash.digest(), 'big')
    if crc_8bit != calculated_crc8:
        raise BadFrameError("CRC - mismatch")


if __name__ == '__main__':
    tag = bitstring_to_bytes('00 0 00001'.replace(' ', ''))
    # tag = b'1'
    length = bitstring_to_bytes('0 0000001'.replace(' ', ''))
    # length = b'1'
    data = 0xFF.to_bytes(1, 'big')
    # data = b'255'

    byte_stream = bytes()
    byte_stream += tag + length + data
    print(byte_stream)

    data_lst = decode_tlv(byte_stream)


