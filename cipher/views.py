from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from .utils import vigenere, playfair, io
from .forms import UploadFileForm

import os
import random

# Create your views here.
def cipher(request):
	context = {
		'form': UploadFileForm()
	}

	if request.method == 'POST':
		plain_text = request.POST['plain_text']
		submit_btn = request.POST['submit_btn']
		cipher = request.POST.get('cipher', False)
		key = request.POST['key']

		form = UploadFileForm(request.POST, request.FILES)

		# Get the name and path of the uploaded file
		filename = str(form['upload'].value())
		filepath = os.path.join(settings.MEDIA_ROOT, filename)

		if cipher or filename != 'None':
			result = None

			if form.is_valid() and filename != 'None':
				if submit_btn == 'encrypt':
					if key:
						# Saving to file system
						fs = FileSystemStorage()
						if filename not in os.listdir(settings.MEDIA_ROOT):
							fs.save(filename, request.FILES['upload'])
						content = io.read_file_as_bytes(filepath)
						encrypted_content = io.encrypt(content, key)
						io.write_file_in_bytes(filepath, encrypted_content)
						context['key'] = key
						context['success'] = 'File encrypted.'
					else:
						messages.info(request, 'Encrypting file requires key.')
				else:
					if key:
						content = io.read_file_as_bytes(filepath)
						decrypted_content = io.decrypt(content, key)
						io.write_file_in_bytes(filepath, decrypted_content)
						context['key'] = key
						context['success'] = 'File decrypted.'
					else:
						messages.info(request, 'Decrypting file requires key.')

			else:
				try:
					if cipher == 'playfair':
						# Using Playfair
						if not key:
							messages.info(request, 'Playfair cipher requires key.')
						else:
							if submit_btn == 'encrypt':
								result = playfair.encrypt(plain_text, key)
							else:
								result = playfair.decrypt(plain_text, key)
					elif cipher == 'vigenere':
						# Using OTP
						if not key:
							cipher = 'One-time Pad'
							rand = random.randint(0, 256)
							key = io.read_file_txt(settings.STATIC_ROOT+'\\file\\key.txt')[rand:rand+len(plain_text)]
						# Using Vigenere
						if submit_btn == 'encrypt':
							result = vigenere.encrypt(plain_text, key)
						else:
							result = vigenere.decrypt(plain_text, key)
					elif cipher == 'ext_vigenere':
						cipher = 'Extended Vigenere'
						# Using extended Vigenere
						if not key:
							messages.info(request, 'Extended Vigenere cipher requires key.')
						else:
							if submit_btn == 'encrypt':
								result = vigenere.extended_encrypt(plain_text, key)
							else:
								result = vigenere.extended_decrypt(plain_text, key)

					context = {
						'plain_text': plain_text,
						'key': key,
						'cipher': cipher.capitalize(),
						'form': UploadFileForm(),
						'result': result
					}
				except Exception as e:
					context['error'] = f'Invalid characters on plain text or key for {cipher.capitalize()} cipher.'
					print(e)
		else:
			context = {
				'plain_text': plain_text,
				'key': key,
				'form': UploadFileForm(),
			}
			messages.info(request, 'Please select a cipher.')

	return render(request, '01_cipher.html', context)