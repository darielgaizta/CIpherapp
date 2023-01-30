'''
Playfair Cipher
'''

import re

ALPHABETS = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def remove_punctuations(string):
	return re.sub(r'[^\w\s]', '', string)

def transform_text(string):
	string = remove_punctuations(''.join(string.split()))
	if len(string) % 2 == 0:
		limit = len(string)
	else:
		limit = len(string) - 1
	for i in range(0, limit, 2):
		# When 'J' is in the plain text
		if string[i] == 'j':
			tmp = list(string)
			tmp[i] = 'i'
			string = ''.join(tmp)
		# When the same characters meet
		if string[i] == string[i+1]:
			new_string = string[:i+1] + 'x' + string[i+1:]
			new_string = transform_text(new_string)
			break
		else:
			new_string = string
	# Add 'x' if the length of the new string is odd		
	if len(new_string) % 2 != 0: new_string += 'x'
	return new_string

def get_bigraph(string):
	string = transform_text(string)
	retval = []
	idx = 0
	for i in range(2, len(string), 2):
		retval.append(string[idx:i])
		idx = i
	retval.append(string[idx:])
	return retval

def generate_key_table(key):
	tab = []
	key = ''.join(key.upper().split()) + ''.join(ALPHABETS)
	for i in range(len(key)):
		# Excluding 'J' in the table
		if key[i] not in tab and key[i] != 'J':
			tab.append(key[i])
	return [tab[i:i+5] for i in range(0, len(tab), 5)]

def search(table, value):
	# Return the indexes of a value from a 2D matrix (table)
	return [(index, row.index(value)) for index, row in enumerate(table) if value in row]

def encrypt(string, key):
	bigraph = get_bigraph(string)
	key_tab = generate_key_table(key)

	retval = ''
	
	for i in range(len(bigraph)):
		bigraph[i] = bigraph[i].replace('J', 'I')
		row1, col1 = search(key_tab, bigraph[i][0].upper())[0]
		row2, col2 = search(key_tab, bigraph[i][1].upper())[0]
		char1 = key_tab[row1][col2]
		char2 = key_tab[row2][col1]
		if row1 == row2:
			# If both characters are in the same row
			if (col1 + 1) > 4: col1 -= 5
			if (col2 + 1) > 4: col2 -= 5
			char1 = key_tab[row1][col1+1]
			char2 = key_tab[row2][col2+1]
			if col1 == 4: char1 = key_tab[row1][0]
			if col2 == 4: char2 = key_tab[row2][0]
		elif col1 == col2:
			# If both characters are in the same column
			if (row1 + 1) > 4: row1 -= 5
			if (row2 + 1) > 4: row2 -= 5
			char1 = key_tab[row1+1][col1]
			char2 = key_tab[row2+1][col2]
			if row1 == 4: char1 = key_tab[0][col1]
			if row2 == 4: char2 = key_tab[0][col2]

		retval += char1 + char2

	return retval

def decrypt(string, key):
	bigraph = get_bigraph(string)
	key_tab = generate_key_table(key)

	retval = ''

	for cipher_pair in bigraph:
		cipher_pair = cipher_pair.replace('J', 'I')

		row1, col1 = search(key_tab, cipher_pair[0].upper())[0]
		row2, col2 = search(key_tab, cipher_pair[1].upper())[0]

		if row1 == row2:
			if col1 - 1 < 0: col1 += 5
			if col2 - 1 < 0: col2 += 5
			retval += key_tab[row1][(col1-1) % 5] + key_tab[row1][(col2-1) % 5]
		elif col1 == col2:
			if row1 - 1 < 0: row1 += 5
			if row2 - 1 < 0: row2 += 5
			retval += key_tab[(row1-1) % 5][col1] + key_tab[(row2-1) % 5][col1]
		else:
			retval += key_tab[row1][col2] + key_tab[row2][col1]

	return retval.replace('X', '-')

if __name__ == '__main__':
	pass