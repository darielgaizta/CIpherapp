'''
Vigenere Cipher
'''

import re

ALPHABETS = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ASCII = ''.join(chr(i) for i in range(256))

def generate_key(string, key):
	key = list(key)
	if len(string) == len(key): return key
	for i in range(len(string) - len(key)):
		key.append(key[i % len(key)])
	return ''.join(key)

def remove_punctuations(string):
	return re.sub(r'[^\w\s]', '', string)

def encrypt(string, key):
	retval = []
	string = remove_punctuations(''.join(string.upper().split()))
	key = generate_key(string, key.upper().replace(' ', ''))
	for i in range(len(string)):
		x = (ALPHABETS.index(string[i]) + ALPHABETS.index(key[i])) % 26
		retval.append(ALPHABETS[x])
	return ''.join(retval)

def decrypt(string, key):
	retval = []
	string = remove_punctuations(''.join(string.upper().split()))
	key = generate_key(string, key.upper().replace(' ', ''))
	for i in range(len(string)):
		x = (ALPHABETS.index(string[i]) - ALPHABETS.index(key[i])) % 26
		retval.append(ALPHABETS[x])
	return ''.join(retval)

def extended_encrypt(string, key):
	retval = []
	key = generate_key(string, key.upper().replace(' ', ''))
	for i in range(len(string)):
		x = (ASCII.index(string[i]) + ASCII.index(key[i])) % 256
		retval.append(ASCII[x])
	return ''.join(retval)

def extended_decrypt(string, key):
	retval = []
	key = generate_key(string, key.upper().replace(' ', ''))
	for i in range(len(string)):
		x = (ASCII.index(string[i]) - ASCII.index(key[i])) % 256
		retval.append(ASCII[x])
	return ''.join(retval)

if __name__ == '__main__':
	pass