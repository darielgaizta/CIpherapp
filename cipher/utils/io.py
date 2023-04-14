'''
Cipher for I/O File
'''

def read_file_txt(filepath):
	with open(filepath, 'r') as file:
		return file.read()

def read_file_as_bytes(filename):
	with open(filename, 'rb') as file:
		return file.read()

def write_file_in_bytes(filename, content):
	with open(filename, 'wb+') as file:
		file.write(content)

def get_extended_key(key, length):
	if len(key) < length:
		key = list(key)
		for i in range(length - len(key)):
			key.append(key[i % len(key)])
		return ''.join(key)
	return key

def encrypt(byte_string, key):
	retval = b''
	# Encode key from chars to bytes
	encoded_key = str.encode(get_extended_key(key, len(byte_string)))
	for i in range(len(byte_string)):
		b = (byte_string[i] + encoded_key[i]) % 256
		retval += bytes([b])

	return retval

def decrypt(byte_string, key):
	retval = b''
	# Encode key from chars to bytes
	encoded_key = str.encode(get_extended_key(key, len(byte_string)))
	for i in range(len(byte_string)):
		b = (byte_string[i] - encoded_key[i]) % 256
		retval += bytes([b])

	return retval

if __name__ == '__main__':
	pass