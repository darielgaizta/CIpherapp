from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from .utils import vigenere, playfair, io
from .forms import UploadFileForm

import os

# Create your views here.
def index(request):
	context = {
		'form': UploadFileForm()
	}

	if request.method == 'POST':
		plain_text = request.POST['plain_text']
		submit_btn = request.POST['submit_btn']
		cipher = request.POST['cipher']
		key = request.POST['key']

		result = None

		form = UploadFileForm(request.POST, request.FILES)

		# Get the name and path of the uploaded file
		filename = str(form['upload'].value())
		filepath = os.path.join(settings.MEDIA_ROOT, filename)

		if form.is_valid() and filename != 'None':
			if submit_btn == 'encrypt':
				# Saving to file system
				fs = FileSystemStorage()
				if filename not in os.listdir(settings.MEDIA_ROOT):
					fs.save(filename, request.FILES['upload'])
				io.encrypt(filepath, io.generate_key())
				context['success'] = 'File encrypted.'
			else:
				if key:
					io.decrypt(filepath, key)
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
						key = io.read_file_txt(settings.STATIC_ROOT+'\\file\\key.txt')[:len(plain_text)]
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

	return render(request, 'index.html', context)