from unittest import TestCase
import AES

input = b'linuslagerhjelm1'
key = b'secretkeybytes19'


class TestAES(TestCase):
    def test_sunny_day_encryption(self):
        expected = 'd17Mm4oZ1yfuIMPds6m0eDLYTQgauSnIy0t/ENKay7A='
        actual = AES.encrypt(input, key)
        self.assertEqual(expected, actual)

    def test_nibbles(self):
        expected = (7, 3)
        actual = AES._nibbles(115)
        self.assertEqual(expected, actual)

    def test_S(self):
        expected = [0x87, 0xEC, 0x4A, 0x8C]
        actual = AES._substitute_bytes([0xEA, 0x83, 0x5C, 0xF0])
        self.assertEqual(expected, actual)
