from unittest import TestCase
from AES import AES
from AES import _g, _sub_bytes, S_box, _shift_rows, _add_round_key, _expand_key, _pad_data, ECB

key = b'abcdefghijklmnop'

class TestAES(TestCase):
    def test_sunny_day_encryption(self):
        expected = bytes([0x29, 0xC3, 0x50, 0x5F, 0x57, 0x14, 0x20, 0xF6, 0x40, 0x22, 0x99, 0xB3, 0x1A, 0x02, 0xD7, 0x3A])
        data = bytes([0x54, 0x77, 0x6F, 0x20, 0x4F, 0x6E, 0x65, 0x20, 0x4E, 0x69, 0x6E, 0x65, 0x20, 0x54, 0x77, 0x6F])
        key = bytes([0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x4B, 0x75, 0x6E, 0x67, 0x20, 0x46, 0x75])
        actual = AES(key)._encrypt_single_block(data)
        self.assertEqual(expected, actual)

    def test_sunny_day_encryption_spec(self):
        data = bytes(bytearray.fromhex('00112233445566778899aabbccddeeff'))
        key = bytes(bytearray.fromhex('000102030405060708090a0b0c0d0e0f'))
        expected = bytes(bytearray.fromhex('69c4e0d86a7b0430d8cdb78070b4c55a'))
        actual = AES(key)._encrypt_single_block(data)
        self.assertEqual(expected, actual)

    def test_sunny_day_decryption(self):
        data = bytes([0x29, 0xC3, 0x50, 0x5F, 0x57, 0x14, 0x20, 0xF6, 0x40, 0x22, 0x99, 0xB3, 0x1A, 0x02, 0xD7, 0x3A])
        key = bytes([0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x4B, 0x75, 0x6E, 0x67, 0x20, 0x46, 0x75])
        expected = bytes([0x54, 0x77, 0x6F, 0x20, 0x4F, 0x6E, 0x65, 0x20, 0x4E, 0x69, 0x6E, 0x65, 0x20, 0x54, 0x77, 0x6F])
        actual = AES(key)._decrypt_single_block(data)
        self.assertEqual(expected, actual)

    def test_sunny_day_decryption_spec(self):
        data = bytes(bytearray.fromhex('69c4e0d86a7b0430d8cdb78070b4c55a'))
        key = bytes(bytearray.fromhex('000102030405060708090a0b0c0d0e0f'))
        expected = bytes(bytearray.fromhex('00112233445566778899aabbccddeeff'))
        actual = AES(key)._decrypt_single_block(data)
        self.assertEqual(expected, actual)

    def test_g(self):
        w = [0x67, 0x20, 0x46, 0x75]
        expected = [0xB6, 0x5A, 0x9D, 0x85]
        actual = _g(w, 0x01)
        self.assertEqual(expected, actual)

    def test_sub_bytes(self):
        state = [
            [0x00, 0x3C, 0x6E, 0x47],
            [0x1F, 0x4E, 0x22, 0x74],
            [0x0E, 0x08, 0x1B, 0x31],
            [0x54, 0x59, 0x0B, 0x1A]
        ]
        expected = [
            [0x63, 0xEB, 0x9F, 0xA0],
            [0xC0, 0x2F, 0x93, 0x92],
            [0xAB, 0x30, 0xAF, 0xC7],
            [0x20, 0xCB, 0x2B, 0xA2],
        ]
        actual = _sub_bytes(state, S_box)
        self.assertEqual(expected, actual)

    def test_shift_rows(self):
        state = [
            [99, 202, 183, 4],
            [9, 83, 208, 81],
            [205, 96, 224, 231],
            [186, 112, 225, 140],
        ]
        expected = [
            [99, 83, 224, 140],
            [9, 96, 225, 4],
            [205, 112, 183, 81],
            [186, 202, 208, 231],
        ]
        actual = _shift_rows(state)
        self.assertEqual(expected, actual)

    def test_add_roundkey(self):
        state = [
            [0xBA, 0x84, 0xE8, 0x1B],
            [0x75, 0xA4, 0x8D, 0x40],
            [0xF4, 0x8D, 0x06, 0x7D],
            [0x7A, 0x32, 0x0E, 0x5D],
        ]
        round_key = [
            [0xE2, 0x91, 0xB1, 0xD6],
            [0x32, 0x12, 0x59, 0x79],
            [0xFC, 0x91, 0xE4, 0xA2],
            [0xF1, 0x88, 0xE6, 0x93],
        ]

        expected = [
            [0x58, 0x15, 0x59, 0xCD],
            [0x47, 0xB6, 0xD4, 0x39],
            [0x08, 0x1C, 0xE2, 0xDF],
            [0x8B, 0xBA, 0xE8, 0xCE],
        ]
        actual = _add_round_key(state, round_key)
        self.assertEqual(expected, actual)

    def test_expand_key(self):
        key = bytes([0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x4B, 0x75, 0x6E, 0x67, 0x20, 0x46, 0x75])
        expected = [
            [[0x54, 0x68, 0x61, 0x74], [0x73, 0x20, 0x6D, 0x79], [0x20, 0x4B, 0x75, 0x6E], [0x67, 0x20, 0x46, 0x75]],
            [[0xE2, 0x32, 0xFC, 0xF1], [0x91, 0x12, 0x91, 0x88], [0xB1, 0x59, 0xE4, 0xE6], [0xD6, 0x79, 0xA2, 0x93]],
            [[0x56, 0x08, 0x20, 0x07], [0xC7, 0x1A, 0xB1, 0x8F], [0x76, 0x43, 0x55, 0x69], [0xA0, 0x3A, 0xF7, 0xFA]],
            [[0xD2, 0x60, 0x0D, 0xE7], [0x15, 0x7A, 0xBC, 0x68], [0x63, 0x39, 0xE9, 0x01], [0xC3, 0x03, 0x1E, 0xFB]],
            [[0xA1, 0x12, 0x02, 0xC9], [0xB4, 0x68, 0xBE, 0xA1], [0xD7, 0x51, 0x57, 0xA0], [0x14, 0x52, 0x49, 0x5B]],
            [[0xB1, 0x29, 0x3B, 0x33], [0x05, 0x41, 0x85, 0x92], [0xD2, 0x10, 0xD2, 0x32], [0xC6, 0x42, 0x9B, 0x69]],
            [[0xBD, 0x3D, 0xC2, 0x87], [0xB8, 0x7C, 0x47, 0x15], [0x6A, 0x6C, 0x95, 0x27], [0xAC, 0x2E, 0x0E, 0x4E]],
            [[0xCC, 0x96, 0xED, 0x16], [0x74, 0xEA, 0xAA, 0x03], [0x1E, 0x86, 0x3F, 0x24], [0xB2, 0xA8, 0x31, 0x6A]],
            [[0x8E, 0x51, 0xEF, 0x21], [0xFA, 0xBB, 0x45, 0x22], [0xE4, 0x3D, 0x7A, 0x06], [0x56, 0x95, 0x4B, 0x6C]],
            [[0xBF, 0xE2, 0xBF, 0x90], [0x45, 0x59, 0xFA, 0xB2], [0xA1, 0x64, 0x80, 0xB4], [0xF7, 0xF1, 0xCB, 0xD8]],
            [[0x28, 0xFD, 0xDE, 0xF8], [0x6D, 0xA4, 0x24, 0x4A], [0xCC, 0xC0, 0xA4, 0xFE], [0x3B, 0x31, 0x6F, 0x26]],
        ]
        actual = _expand_key(key, 10)
        self.assertEqual(expected, actual)

    def test_pad_incomplete_block(self):
        data = b'abcdefghijklmno'
        expected = b'abcdefghijklmno\x01'
        actual = _pad_data(data)
        self.assertEqual(expected, actual)

    def test_pad_complete_block(self):
        data = b'abcdefghijklmnop'
        expected = b'abcdefghijklmnop\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
        actual = _pad_data(data)
        self.assertEqual(expected, actual)

    def test_pad_empty_block(self):
        data = b''
        expected = b'\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
        actual = _pad_data(data)
        self.assertEqual(expected, actual)

    def test_pad_and_encrypt_single_block_ECB(self):
        data = b'abcdefghijklmno'
        expected = b'\xd7={E2\x9df\xf7\xfe\xb5\xa5\x97\x1c\xaex\xac'
        actual, _ = AES(key, ECB).encrypt(data)
        self.assertEqual(expected, actual)

    def test_encrypt_multiple_blocks_ECB(self):
        data = b'abcdefghijklmnopabcdefghijklmnop'
        expected = b'\xa9\x13)\xaf\x99\xa7\x8d\x02\xae\xc1|PwW\xaa\xef\xa9\x13)\xaf\x99\xa7' \
                   b'\x8d\x02\xae\xc1|PwW\xaa\xef\x8ed\xce\x87?\x17M\xbb$#\xfc\xd8\x14X\x0e\x15'

        actual, _ = AES(key, ECB).encrypt(data)
        self.assertEqual(expected, actual)

    def test_decrypt_multiple_blocks_ECB(self):
        data = b'\xa9\x13)\xaf\x99\xa7\x8d\x02\xae\xc1|PwW\xaa\xef\xa9\x13)\xaf\x99\xa7' \
               b'\x8d\x02\xae\xc1|PwW\xaa\xef\x8ed\xce\x87?\x17M\xbb$#\xfc\xd8\x14X\x0e\x15'

        expected = b'abcdefghijklmnopabcdefghijklmnop'
        actual = AES(key, ECB).decrypt(data)
        self.assertEqual(expected, actual)

    def test_encrypt_multiple_blocks_CBC(self):
        data = b'abcdefghijklmnop'
        iv = b'somerandominvect'
        expected = b'\xc6n\x1b\xcbP\x99-4\xb8\xbc\x9c\x0fy6KQ\xec\xee\xd0+\xb5\xf1\xd3\xb4\xcf\xa2\x92j\xd2;\xcc\xf4'
        actual, _ = AES(key).encrypt(data, iv)
        self.assertEqual(expected, actual)

    def test_decrypt_single_block_CBC(self):
        iv = b'somerandominvect'
        data = b'\xc6n\x1b\xcbP\x99-4\xb8\xbc\x9c\x0fy6KQ'
        expected = b'abcdefghijklmnop'
        actual = AES(key)._decrypt_CBC([data], iv)
        self.assertEqual(expected, actual)

    def test_decrypt_multiple_blocks_CBC(self):
        iv = b'somerandominvect'
        data = b'\xc6n\x1b\xcbP\x99-4\xb8\xbc\x9c\x0fy6KQ\xec\xee\xd0+\xb5\xf1\xd3\xb4\xcf\xa2\x92j\xd2;\xcc\xf4'
        expected = b'abcdefghijklmnop'
        actual = AES(key).decrypt(data, iv)
        self.assertEqual(expected, actual)

    def test_assignment_data(self):
        data = AES(key).encrypt(b'Introduction to Computer Security')
