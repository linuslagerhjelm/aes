#!/usr/local/bin/python3
import sys
import argparse
import signal
import getpass

error = lambda msg: sys.exit(msg)

def sigint_handler(sig, frame):
  print("\r" + (' ' * 80) + "\rGood bye ☺️")
  sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

parser = argparse.ArgumentParser(description='AESCrypt - A tool to encrypt and decrypt data using the AES algorithm.')
parser.add_argument('--key', type=str, help='The key to use, exists only to allow scripting. Should be left blank if used interactively.')
parser.add_argument('-f', type=str, help='Encrypts the content of the specified file, set the -o flag to specify a different output file.')
parser.add_argument('-o', type=str, help='A file to put the encrypted data into.')

args = parser.parse_args()

key = args.key if args.key else getpass.getpass("Key (16 characters): ")
if len(key) != 16:
  error("Expected key to be 16 characters")

interactive_mode() if not args.f else file_mode(args)

def file_mode(args):
  return

def interactive_mode():
  return
