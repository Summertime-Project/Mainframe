from typing import Tuple, Optional, List

from communication.parser_types import TagType, Tag, TagForm, ByteData


def parse_tag(byte_stream: bytes) -> Tuple[Tag, bytes]:
    tag = byte_stream[0]

    tag_type = TagType((tag & 192) >> 6)
    form = TagForm((tag & (1 << 5)) >> 5)
    number = tag & 0b11111

    if number == 31:
        number = 0
        i = 1
        while True:
            number <<= 7
            number |= byte_stream[i] & 127
            i += 1
            if number & 128 == 0:
                break
        byte_stream = byte_stream[i:]
    else:
        byte_stream = byte_stream[1:]

    return Tag(tag_type, form, number), byte_stream


def parse_length(byte_stream: bytes) -> Tuple[int, bytes]:
    length = byte_stream[0]

    if length & 128 != 0:
        n = length & 127  # 7 first bits
        length = 0
        for i in range(n):
            length <<= 8  # shift old value by 8 bits
            length |= byte_stream[i + 1]
        byte_stream = byte_stream[n:]

    return length, byte_stream[1:]


def parse_tlv(byte_stream: bytes) -> Tuple[ByteData, Optional[bytes]]:
    tag, byte_stream = parse_tag(byte_stream)
    length, byte_stream = parse_length(byte_stream)

    if tag.form == TagForm.PRIMITIVE:
        value = byte_stream[:length]
        byte_stream = byte_stream[length:]
    else:  # TODO - implement constructed data
        # value, bytes_stream = parse_tlv(byte_stream)
        raise NotImplementedError()

    return ByteData(tag, value), byte_stream


def parse_data(byte_stream: bytes) -> List[ByteData]:
    data_lst = []
    while True:
        data, byte_stream = parse_tlv(byte_stream)
        data_lst.append(data)
        if len(byte_stream) == 0:
            break
    return data_lst
