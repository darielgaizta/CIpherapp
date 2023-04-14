'''
Digital Signature with RSA
[1] Hash message M: H(M) = h
[2] Encrypt hashed message with private key: S = E_sk(h) mod n
[3] Output M + S, so that receiver can see the message and the signature

Verify Message
[1] Hash message M: H(M) = h
[2] Decrypt encrypted hashed message (S) with sender's public key: h' = D_pk(S) mod n
[3] Compare h with h'
    If both are the same, then the message M is authentic (not modified).
    Else, it's not authentic.

Generate RSA Key
[1] Pick two prime number p and q
[2] Calculate n: n = p * q
[3] Calculate phi(n): phi(n) = (p-1) * (q-1)
[4] Pick a random whole number e that is prime relative to phi(n)
[5] Calculate decryption key d with Euclidean algorithm :') until we have d is a whole number
    d = (1 + (k * phi(n))) / e

"Bang, udah bang..."
'''

import math
import hashlib

NUMBERS = '0123456789'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

CHARPOOL = list(ALPHABET + ALPHABET.lower() + NUMBERS)

'''
Read File as Bytes
'''
def read_file_in_bytes(filename):
	with open(filename, 'rb') as file:
		return file.read()


'''
Write File as Bytes
'''
def write_file_in_bytes(filename, content):
	with open(filename, 'wb') as file:
		file.write(content)


'''
Check Co Prime
Check if two numbers are coprime to each other
'''
def check_co_prime(a, b):
    return math.gcd(a, b) == 1


'''
Generate RSA Key
Get a pair of public key and private key
'''
def generate_rsa_key(p, q, e=None):
    n, phi, k = p * q, (p - 1) * (q - 1), 1

    if not e:  
        i = 2
        # Get the e starting from i = 2
        while not check_co_prime(i, phi):
            i += 1
        e = i
    
    # Calculate d
    d = (1 + (k * phi)) // e
    while ((1 + (k * phi)) / e) != d:
        k += 1
        d = (1 + (k * phi)) // e
    
    return ([e, n], [d, n])


'''
Hash Message
Hash message using SHA-3 and return the hashed message
'''
def hash_message(encoded_string):
    hashed_message = hashlib.new('sha3_512', encoded_string)
    return hashed_message.hexdigest()


'''
Sign Digital Signature
Sign digital signature using private key
'''
def sign_digital_signature(message, key):
    signature = int(message, 16)**key[0] % key[1]
    return '<ds>' + str(signature) + '</ds>'


'''
Verify Signature
Verify Signature using public key
'''
def verify_signature(hashed_message, signature, key):
    signature = signature.replace(b'<ds>', b'').replace(b'</ds>', b'')
    return int(signature)**key[0] % key[1] == int(hashed_message, 16) % key[1]
    

'''
Get Signature
Get signature of a content
'''
def scan_content(content, tag=b'<ds>'):
    try:
        i = content.index(tag)
        return (content[:i], content[i:])
    except Exception as e:
        return None


if __name__ == '__main__':
    filename = 'test.txt'

    # Pick random prime number
    p, q = 47, 71
    
    # Generate RSA Key
    private_key, public_key = generate_rsa_key(p, q)
    print('Keys:', private_key, public_key)

    # Read content
    content = read_file_in_bytes(filename=filename)
    print('Content:', content)
    content, signature = scan_content(content=content)
    print('Signature:', signature)

    # # Encryption
    hashed_content = hash_message(encoded_string=content)
    # encrypted_message = sign_digital_signature(hashed_content, private_key)

    # print('Hashed:', hashed_content)
    # print('Encrypted:', encrypted_message)

    # # Attach digital signature
    # new_content = content + encrypted_message.encode('utf-8')
    # write_file_in_bytes(filename=filename, content=new_content)

    # Decryption
    decrypted_message = verify_signature(hashed_content, signature, public_key)
    print('Authentic:', decrypted_message)