#!/usr/local/bin/python3
import sys
import os
import argparse
import signal
import getpass
import base64
import hashlib
from AES import AES


SALT_LEN = 64
BLOCK_LEN = 16
KEY_LEN = 32


def error(msg): sys.exit(msg)


def get_file_content(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except IOError:
        error('Unable to open the specified file')


def write_file(filename, content):
    try:
        with open(filename, 'wb+') as f:
            f.write(content)
    except IOError:
        error('Unable to write to file')


def derive_key(password: bytes, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac(
        hash_name='sha512',
        password=password,
        salt=salt,
        iterations=100000,
        dklen=KEY_LEN
    )
    return key


def sigint_handler(_, __):
    print("\r" + (' ' * 80) + "\rGood bye ☺️")
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)


def interactive_mode(aes):
    exit("Interactive mode is currently not supported, please specify an input file")


def decrypt(data, password):
    data = base64.b64decode(data)
    salt, iv, ciphertext = data[:SALT_LEN], data[SALT_LEN:SALT_LEN + BLOCK_LEN], data[SALT_LEN+BLOCK_LEN:]
    return AES(derive_key(password.encode(), salt)).decrypt(ciphertext, iv)


def encrypt(data, password):
    salt = os.urandom(64)
    ciphertext, iv = AES(derive_key(password.encode(), salt)).encrypt(data)
    return base64.b64encode(salt + iv + ciphertext)


def file_mode(password, args):
    data = get_file_content(args.f)
    if args.d:
        res = decrypt(data, password)
    else:
        res = encrypt(data, password)
    outfile = args.f if not args.o else args.o
    write_file(outfile, res)


parser = argparse.ArgumentParser(description='AESCrypt - A tool to encrypt and decrypt data using the AES algorithm.')
parser.add_argument('--passwd', type=str, help='The password to use, exists only to allow scripting. '
                                               'Should be left blank if used interactively.'
                                               'Even in scripts, the value of this flag should not be set directly'
                                               'but rather through, e.g. an environment variable.')
parser.add_argument('-f', type=str, help='Encrypts the content of the specified file, set the -o flag to specify a different output file.')
parser.add_argument('-o', type=str, help='A file to put the encrypted data into.')
parser.add_argument('-d', action='store_true', help='Use decrypt mode. Can be used when starting interactive mode as well')

arguments = parser.parse_args()

passwd = arguments.passwd if arguments.passwd else getpass.getpass("Password: ")
if not passwd:
    error("Password can not be blank!")

interactive_mode(passwd) if not arguments.f else file_mode(passwd, arguments)
