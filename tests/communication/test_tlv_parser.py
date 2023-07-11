import unittest
from communication import tlv_parser


class TestTlvParser(unittest.TestCase):
    def test_decode_crc8_checking(self):
        string = "123456789"
        bytes_stream = bytes(string, 'utf8')

        crc8_result = 0xF4
        bytes_stream += crc8_result.to_bytes(1, 'big')

        try:
            tlv_parser.decode(bytes_stream)
        except tlv_parser.BadFrameError:
            self.fail("BadFrameError: exception thrown")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
