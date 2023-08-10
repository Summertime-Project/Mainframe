import unittest
from communication import parser


class TestTlvParse(unittest.TestCase):
    def test_parse_length(self):
        # 1 byte length
        bytes_stream = bytearray(b'\x03\x04\x05\xFF')
        length, bytes_stream_result = parser.parse_length(bytes_stream)

        self.assertEqual(3, length)
        self.assertEqual(bytes_stream[1:], bytes_stream_result)

        # 3 byte length
        bytes_stream = bytearray()
        bytes_stream.extend(b'\x83\x01\x00\x01\xFF\x12')

        length, bytes_stream_result = parser.parse_length(bytes_stream)
        self.assertEqual(65537, length)
        self.assertEqual(bytes_stream[4:], bytes_stream_result)

    def test_parse_tag(self):
        bytes_stream = bytearray(b'\x01\x02\xFF')
        tag, bytes_stream_result = parser.parse_tag(bytes_stream)

        correct_tag = parser.Tag(0, 0, 1)
        self.assertEqual(correct_tag, tag)
        self.assertEqual(bytes_stream[1:], bytes_stream_result)

        bytes_stream = bytearray(b'\xED\xFF\xA5')
        tag, bytes_stream_result = parser.parse_tag(bytes_stream)

        correct_tag = parser.Tag(3, 1, 13)
        self.assertEqual(correct_tag, tag)
        self.assertEqual(bytes_stream[1:], bytes_stream_result)

        # tag > 31
        bytes_stream = bytearray(b"\x5F\x28")

        self.assertEqual(2, len(bytes_stream))
        tag, bytes_stream_result = parser.parse_tag(bytes_stream)

        correct_tag = parser.Tag(1, 0, 40)
        self.assertEqual(correct_tag, tag)
        self.assertEqual(bytes_stream[2:], bytes_stream_result)

    def test_parse_tlv(self):
        bytes_stream = bytearray(b'\x01\x01\xFF\x03\x99')
        data, bytes_stream_result = parser.parse_tlv(bytes_stream)

        correct_data = parser.ByteData(parser.Tag(0, 0, 1), b'\xFF')
        self.assertEqual(correct_data, data)
        self.assertEqual(bytes_stream[3:], bytes_stream_result)

    def test_parse_data(self):
        bytes_stream = bytearray(b'\x01\x01\xAF\x02\x01\xAB')
        data_lst = parser.parse_data(bytes_stream)

        correct_data = [parser.ByteData(parser.Tag(0, 0, 1), b'\xAF'), parser.ByteData(parser.Tag(0, 0, 2), b'\xAB')]
        self.assertEqual(correct_data, data_lst)


if __name__ == '__main__':
    unittest.main()
