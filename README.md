# AES

A pure python implementation of AES written with the goal to resemble the 
[spec](https://csrc.nist.gov/csrc/media/publications/fips/197/final/documents/fips-197.pdf) as closely as possible and still be quite pythonic.

## Security

This library is completely compliant with the AES spec and, if configured correctly,
provides cryptography that is secure enough for information up to TOP SECRET
level as per [recommendation](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard#Security) 
from the U.S. Government. 

Two things to note about this version of the implementation is that it is
potentially susceptible to [cache timing](https://cr.yp.to/antiforgery/cachetiming-20050414.pdf)
attacks and does not use [authenticated encryption](https://cr.yp.to/antiforgery/cachetiming-20050414.pdf).

These issues are intended to be addressed in future versions of the code but for
the moment, if your threat model include _side channel_ attacks or your application
need to send encrypted data over the network, other libraries may be a better fit.


## Usage

````python
import os
from AES import AES

key = os.urandom(32)
aes = AES(key)
cipher_text, iv = aes.encrypt(b'Some secret message')
plain_text = aes.decrypt(cipher_text, iv)
````

## Features
The library supports the following key sizes/modes/operations:

- 128 bit keys
- 192 bit keys
- 256 bit keys
- ECB Mode
- CBC Mode
- PKCS7 Padding

## CLI

This project comes with a cli tool that wraps the library for command line usage.
The usage of the CLI is of course about as secure as using the library code directly,
apart from that the CLI implements a cryptographic schema that uses the most
secure configuration possible of the library.
 
### Usage

 Following is the help output from the CLI:

````bash
 usage: AESCrypt.py [-h] [--key KEY] [-f F] [-o O] [-d]

AESCrypt - A tool to encrypt and decrypt data using the AES algorithm.

optional arguments:
  -h, --help  show this help message and exit
  --key KEY   The key to use, exists only to allow scripting. Should be left
              blank if used interactively.
  -f F        Encrypts or decrypts the content of the specified file, set the -o flag to
              specify a different output file.
  -o O        A file to put the output into.
  -d          Use decrypt mode. Can be used when starting interactive mode as
              well
````

For example: to encrypt the file `test.txt`:

````bash
./AESCrypt.py  -f test.txt
````

And to decrypt the same file:

````bash
./AESCrypt.py  -df test.txt
````

### Configuration
In order to provide maximal security, this tool uses some configurations that 
could be of interest to state here to allow for external evaluation/validation
of its security. It uses the largest possible key sizes namely 256 bits. 
It encrypts everything using CBC mode with a new  cryptographically secure IV 
for each encryption. Furthermore, it uses a key derivation function, 
PBKDF2 (SHA-512) to map user passwords into strong keys to be used for encryption.
Each key is generated using a salt from 64 cryptographically secure random bits. 

### TODO (CLI)

CLI specific things, yet to be implemented:

- ~~Add a KDF so that the user can use any password~~
- Implement interactive mode
- IO to/from stdin/stdout to allow piping
- Update KDF to scrypt
