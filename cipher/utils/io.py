'''
Cipher for I/O File
'''

import os
from pathlib import Path
from django.conf import settings
from cryptography.fernet import Fernet

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

if __name__ == '__main__':
	pass