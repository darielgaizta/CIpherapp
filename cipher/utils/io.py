'''
Cipher for I/O File
'''

import os
from pathlib import Path
from django.conf import settings
from cryptography.fernet import Fernet

from . import vigenere

ASCII = ''.join(chr(i) for i in range(512))

def read_file_txt(filepath):
	with open(filepath, 'r') as file:
		return file.read()

def read_file_bin(filepath):
	with open(filepath, 'rb') as file:
		return file.read()

def generate_key():
	key = Fernet.generate_key()
	with open(settings.DOTENV_PATH, 'wb') as filekey:
		filekey.write(key)
	return key

# Encrypt using Fernet
def encrypt(filename, key):
	fernet = Fernet(key)
	with open(filename, 'rb') as file:
		original = file.read()
	encrypted = fernet.encrypt(original)
	with open(filename, 'wb') as encrypted_file:
		encrypted_file.write(encrypted)

# Decrypt using Fernet
def decrypt(filename, key):
	fernet = Fernet(key)
	with open(filename, 'rb') as encrypted_file:
		encrypted = encrypted_file.read()
	decrypted = fernet.decrypt(encrypted)
	with open(filename, 'wb') as decrypted_file:
		decrypted_file.write(decrypted)

def extended_encrypt(filename, key):
	encoded = b''

	with open(filename, 'rb') as file:
		file_in_bytes = file.read()

	key = vigenere.generate_key(file_in_bytes, key)

	for i in range(len(file_in_bytes)):
		c = (file_in_bytes[i] + ord(key[i])) % 256
		encoded += str(c).encode()

	with open(filename, 'wb') as encrypted_file:
		encrypted_file.write(encoded)


def extended_decrypt(filename, key):
	decoded = b''

	with open(filename, 'rb') as file:
		file_in_bytes = file.read()

	key = vigenere.generate_key(file_in_bytes, key)

	for i in range(len(file_in_bytes)):
		p = (file_in_bytes[i] - ord(key[i])) % 256
		decoded += str(p).encode()

	with open(filename, 'wb') as decrypted_file:
		decrypted_file.write(decoded)

if __name__ == '__main__':
	pass