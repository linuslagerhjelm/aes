from collections import deque
from functools import reduce

ECB = 1
CBC = 2


S_box = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
]


def _nibbles(byte: int) -> tuple:
    """
    Returns the nibbles to the provided byte. I.e., a tuple where first value is an int corresponding
    to the first four bits of the byte and the second value, the second halves of the bits.
    :param byte: the byte to split
    :return: tuple containing the first and second halves of bits as ints
    """
    b = list(bin(byte))[2:]
    b = (['0'] * (len(b) % 2)) + b
    first = "".join(b[0:int(len(b) / 2)])
    second = "".join(b[int(len(b) / 2):])
    return int(first, 2), int(second, 2)


def _g(block):
    block = deque(block)
    block.rotate(-1)


def __chunk(arr, n):
    return [arr[i * n:(i + 1) * n] for i in range((len(arr) + n - 1) // n)]


def __sub_byte(b):
    b = hex(b)[2:]
    if len(b) == 1:
        b = '0' + b
    row, col = list(b)
    return S_box[int(row, 16)][int(col, 16)]


def _sub_bytes(state):
    new_mat = []
    for row in state:
        new_row = []
        for v in row:
            new_row.append(__sub_byte(v))
        new_mat.append(new_row)
    return new_mat


def __shift_row(row, n):
    return row[-n:] + row[:-n]


def _shift_rows(state):
    new_state = []
    n = 0
    for row in state:
        new_state.append(__shift_row(row, -n))
        n += 1
    return new_state


def __bit_string(byte: int) -> str:
    """
    Converts a byte to its corresponding bit-string
    :param byte: the byte to convert
    :return: a string of 1 and 0:s
    """
    bitstring = bin(int(hex(byte), base=16))[2:]
    pad = '0' * (8 % len(bitstring))
    return pad + bitstring


def __transpose(matr: list) -> list:
    """
    Performs a matrix transposition on a list of lists
    :param matr: the list of lists to transpose
    :return: a transposed list of lists
    """
    return list(map(list, zip(*matr)))


def __xor(l1: str, l2: str) -> str:
    """
    Performs xor between two bit strings
    :param l1: lhs string
    :param l2: rhs string
    :return: the result of lhs XOR rhs
    """
    return "".join(map(str, [int(int(a) != int(b)) for a, b in zip(l1, l2)]))


fix_mat = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02],
]


def __mult_3(v: int) -> str:
    """
    Performs multiplication between v and the byte 0x03
    :param v: the byte to multiply
    :return: the result of v * 0x03 as a binary string
    """
    return __xor(__mult_2(v), __bit_string(v))


def __mult_2(v: int) -> str:
    """
    Performs multiplication between v and the byte 0x02
    :param v: the byte to multiply
    :return: the result of v * 0x02 as a binary string
    """
    res = v << 1
    if v & 0x80:
        bs = __bit_string((res ^ 0x1B) & 0xFF)
    else:
        bs = __bit_string(res)

    return bs


def __mix_column(col):
    new_col = []
    for f in fix_mat:
        bits = []
        for v1, v2 in zip(f, col):
            if v1 == 0x03:
                bs = __mult_3(v2)
            elif v1 == 0x02:
                bs = __mult_2(v2)
            else:
                bs = __bit_string(v2)
            bits.append(bs)

        new_col.append(int(reduce(__xor, bits), 2))
    return new_col


def _mix_columns(state):
    new_state = []
    columns = __transpose(state)
    for col in columns:
        new_col = __mix_column(col)
        new_state.append(new_col)
    return __transpose(new_state)


def _add_roundkey(state, roundkey):
    new_state = []
    for r1, r2 in zip(state, roundkey):
        new_col = []
        for v1, v2 in zip(r1, r2):
            new_col.append(v1 ^ v2)
        new_state.append(new_col)
    return new_state


def _round(state, expanded_key):
    state = _sub_bytes(state)
    state = _shift_rows(state)
    state = _mix_columns(state)
    return _add_roundkey(state, expanded_key)


def encrypt(input: bytes, key: bytes, mode: int = CBC) -> bytes:
    """
    Encrypts a single block of data using the AES algorithm as
    described by: https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf
    :param input:
    :param key:
    :param mode:
    :return:
    """
    # key_rounds = __chunk(list(key), 4)

    # expanded_key = key_expansion()
    # add_roundkey()
    # for n in range(rounds - 1):
    #   round(state, expanded_key[n])
    # final_round(state, expanded_key[-1])

    return b''


def decrypt():
    return
