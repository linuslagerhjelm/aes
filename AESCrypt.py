#!/usr/local/bin/python3
import sys
import argparse
import signal
import getpass
import base64
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

def sigint_handler(sig, frame):
  print("\r" + (' ' * 80) + "\rGood bye ☺️")
  sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

def interactive_mode(aes):
  return

def decrypt_file(aes, f_in, f_out):
  data = str.encode(get_file_content(f_in))
  data = base64.b64decode(data)
  iv, ciphertext = data[:16], data[16:]
  plaintext = aes.decrypt(ciphertext, iv).decode()
  outfile = f_in if not f_out else f_out
  write_file(outfile, plaintext)


def encrypt_file(aes, f_in, f_out):
  data = get_file_content(f_in)
  ciphertext, iv = aes.encrypt(str.encode(data))
  res = base64.b64encode(iv + ciphertext).decode()
  outfile = f_in if not f_out else f_out
  write_file(outfile, res)

def file_mode(aes, args):
  if args.d:
    decrypt_file(aes, args.f, args.o)
  else:
    encrypt_file(aes, args.f, args.o)

parser = argparse.ArgumentParser(description='AESCrypt - A tool to encrypt and decrypt data using the AES algorithm.')
parser.add_argument('--key', type=str, help='The key to use, exists only to allow scripting. Should be left blank if used interactively.')
parser.add_argument('-f', type=str, help='Encrypts the content of the specified file, set the -o flag to specify a different output file.')
parser.add_argument('-o', type=str, help='A file to put the encrypted data into.')
parser.add_argument('-d', action='store_true', help='Use decrypt mode. Can be used when starting interactive mode as well')

args = parser.parse_args()

key = args.key if args.key else getpass.getpass("Key (16 characters): ")
if len(key) != 16:
  error("Expected key to be 16 characters")

aes = AES(str.encode(key))
interactive_mode(aes) if not args.f else file_mode(aes, args)
