'''
Stream Cipher: RC4
'''

import base64

def random_key(k):
    list_key = []
            
    for i in range (len(k)):
        list_key.append(k[i])
        
    n = (len(list_key)%5)
        
    for i in range(n):
        last_element = list_key[-1]

        for j in range(len(list_key)-1, 0, -1):
            list_key[j] = list_key[j-1]

        list_key[0] = last_element
        
    random_key = ''.join(list_key)
    return random_key

# Read file as bytes
# filename : string
def read_file_as_bytes(filename):
	with open(filename, 'rb') as file:
		return file.read()

# Write file in bytes
# filename : string
# content : byte-string
def write_file_in_bytes(filename, content):
	with open(filename, 'wb') as file:
		file.write(content)

# Reduplicate key to the same length as the plain text
# key : byte-string/string
# length : int
def get_extended_key(key, length):
	if len(key) < length:
		key = list(key)
		for i in range(length - len(key)):
			key.append(key[i % len(key)])
		return ''.join(key)
	return key

# Swap the position of l[i] and l[j]
# l : list
# i, j : int
def swap_element_in_list(l, i, j):
	temp = l[i]
	l[i] = l[j]
	l[j] = temp

# Key-scheduling Algorithm (KSA)
# k : byte-string
def key_scheduling(k):
	s, j = [i for i in range(256)], 0

	for i in range(256):
		j = (j + s[i] + ord(k[i % len(k)])) % 256
		swap_element_in_list(s, i, j)

	return s

# Pseudo-random Generation Algorithm (PRGA)
# p : byte-string
# s : array of decimal
def pseudo_random_generation(p, s):
	retval = []

	i, j = 0, 0

	for k in range(len(p)):
		i = (i + 1) % 256
		j = (j + s[i]) % 256
		swap_element_in_list(s, i, j)
		t = (s[i] ^ s[j]) % 256
		u = s[t]
		c = u ^ ord(p[k])
		retval.append(c)
	
	return retval

# Encrypt as bytes of ascii characters
# p, k : byte-string
# toBase64 : Boolean
def encrypt(p, k, toBase64=False):
	j = 0
	vigenere_key = extended_vigenere_encrypt(random_key(k), k)
	s = key_scheduling(k)

	for j in range(256):
		s[j] = s[j] ^ ord(vigenere_key[j % len(vigenere_key)])
	
	b = pseudo_random_generation(p, s)

	# Convert decimal to byte-string
	byte_string = b''.join([bytes([i]) for i in b])
	
	# if toBase64:
	#  	# Return string plain text as base64
	#  	return base64.b64encode(byte_string).decode()
	
	return byte_string.decode('latin-1')

# Decrypt byte-string/base64 as bytes
# p, k : byte-string
# fromBase64 : Boolean
def decrypt(p, k, fromBase64=False):
	# if fromBase64:
	#  	p = base64.b64decode(p)
	s = key_scheduling(k)

	vigenere_key = extended_vigenere_encrypt(random_key(k), k)

	for j in range(256):
		s[j] = s[j] ^ ord(vigenere_key[j % len(vigenere_key)])

	b = pseudo_random_generation(p, s)

	#Convert decimal to byte-string
	byte_string = b''.join([bytes([i]) for i in b])
	
	return byte_string

def extended_vigenere_encrypt(p, k):
	retval = b''
	encoded_str = p.encode(encoding='ascii')
	encoded_key = generate_key(p, k).encode(encoding='ascii')
	for i in range(len(encoded_str)):
		b = (encoded_str[i] + encoded_key[i]) % 256
		retval += bytes([b])
	return retval.decode('latin-1')

def generate_key(string, key):
	if len(string) == len(key): return key
	key = list(key)
	for i in range(len(string) - len(key)):
		key.append(key[i % len(key)])
	return ''.join(key)

# Main driver
if __name__ == '__main__':
	plain = str(input("Masukan plaintext : "))
	key = str(input("Masukan key : "))
	hasil = encrypt(plain, key)
	print("hasil encrypt : ", hasil)
	print('')
	hasil2 = decrypt(hasil, key)
	print("hasil decrypt : ", hasil2.decode('latin-1'))

