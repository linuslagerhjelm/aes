# AES

A pure python implementation of AES written with the goal to resemble the 
spec as closely as possible and still be quite pythonic.

## Security
Do **not** use this library for anything that hsa to do with security. Although
it is compliant with the spec, this is an implementation written for educational
purposes and consequently, no measures has been taken to make the implementation
resistant to side channel attacks etc. 

## Usage
````python
import os
from AES import AES

key = os.urandom(16)
aes = AES(key)
cipher_text, iv = aes.encrypt(b'Some secret message')
plain_text = aes.decrypt(cipher_text, iv)
````

## Features
 - ~~128 bit keys~~
 - 192 bit keys
 - 256 bit keys
 - ECB Mode
 - CBC Mode
 - PKCS7 Padding