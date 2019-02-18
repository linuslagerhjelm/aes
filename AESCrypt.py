#!/usr/local/bin/python3
import sys
import os
import argparse
import signal
import getpass
import base64
import hashlib
from AES import AES

error = lambda msg: sys.exit(msg)

def get_file_content(filename):
  try:
    with open(filename) as f:
      return f.read()
  except IOError:
      error('Unable to open the specified file')

def write_file(filename, content):
  try:
    with open(filename, 'w+') as f:
      f.write(content)
  except IOError:
    error('Unable to write to file')

def derive_key(password: str, salt: bytes) -> tuple:
  key = hashlib.scrypt(
    password=password,
    salt=salt,
    n=1<<17,
    r=8,
    p=1,
    dklen=16
  )
  return key, salt

def sigint_handler(sig, frame):
  print("\r" + (' ' * 80) + "\rGood bye ☺️")
  sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

def interactive_mode(aes):
  exit("Interactive mode is currently not supported, please specify an input file")

def decrypt_file(password, f_in, f_out):
  data = str.encode(get_file_content(f_in))
  data = base64.b64decode(data)
  salt, iv, ciphertext = data[:16], data[16:32], data[16:]
  plaintext = AES(derive_key(password, salt)).decrypt(ciphertext, iv).decode()
  outfile = f_in if not f_out else f_out
  write_file(outfile, plaintext)


def encrypt_file(password, f_in, f_out):
  key, salt = derive_key(password, os.urandom(64))
  data = get_file_content(f_in)
  ciphertext, iv = AES(key).encrypt(str.encode(data))
  res = base64.b64encode(salt + iv + ciphertext).decode()
  outfile = f_in if not f_out else f_out
  write_file(outfile, res)

def file_mode(password, args):
  if args.d:
    decrypt_file(password, args.f, args.o)
  else:
    encrypt_file(password, args.f, args.o)

parser = argparse.ArgumentParser(description='AESCrypt - A tool to encrypt and decrypt data using the AES algorithm.')
parser.add_argument('--passwd', type=str, help='The password to use, exists only to allow scripting. Should be left blank if used interactively.')
parser.add_argument('-f', type=str, help='Encrypts the content of the specified file, set the -o flag to specify a different output file.')
parser.add_argument('-o', type=str, help='A file to put the encrypted data into.')
parser.add_argument('-d', action='store_true', help='Use decrypt mode. Can be used when starting interactive mode as well')

args = parser.parse_args()

password = args.passwd if args.passwd else getpass.getpass("Password: ")
if not password:
  error("Password can not be blank!")

interactive_mode(password) if not args.f else file_mode(password, args)
