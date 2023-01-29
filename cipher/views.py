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

		files = []

		if form.is_valid():
			# Get the name and path of the uploaded file
			filename = str(form['upload'].value())
			filepath = os.path.join(settings.MEDIA_ROOT, filename)
			
			if submit_btn == 'encrypt':
				# Saving to file system
				fs = FileSystemStorage()
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
			if cipher == 'playfair':
				if not key:
					messages.info(request, 'Playfair cipher requires key.')
				if submit_btn == 'encrypt':
					result = playfair.encrypt(plain_text, key)
				else:
					result = playfair.decrypt(plain_text, key)
			elif cipher == 'vigenere':
				# Using OTP
				if not key:
					key = io.read_file_txt(settings.STATIC_ROOT+'\\file\\key.txt')[:len(plain_text)]
				# Using Vigenere
				print('KEY', key)
				if submit_btn == 'encrypt':
					result = vigenere.encrypt(plain_text, key)
				else:
					result = vigenere.decrypt(plain_text, key)

			context = {
				'plain_text': plain_text,
				'key': key,
				'cipher': cipher.capitalize(),
				'form': UploadFileForm(),
				'result': result
			}

	return render(request, 'index.html', context)