import unittest
from communication.decode_primitve import decode_int, decode_bool, DecodeError, decode_real


class DecodePrimitiveTest(unittest.TestCase):
    def test_decode_bool(self):
        value = b'\xFF'
        x = decode_bool(value)
        self.assertEqual(True, x)

        value = b'\x00'
        x = decode_bool(value)
        self.assertEqual(False, x)

        value = bytes(0x10)
        self.assertRaises(DecodeError, decode_bool, value)

    def test_decode_int(self):
        value = b'\x48'
        x = decode_int(value)
        self.assertEqual(72, x)

    def test_decode_real(self):
        value = b'\x80\x00\x0A'
        x = decode_real(value)
        self.assertEqual(10.0, x)


if __name__ == '__main__':
    unittest.main()
