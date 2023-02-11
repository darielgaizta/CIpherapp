from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from .utils import rc4
from .forms import UploadFileForm

import os

# Create your views here.
def stream_cipher(request):
	context = {
		'form': UploadFileForm()
	}

	if request.method == 'POST':
		plain_text = request.POST['plain_text']
		submit_btn = request.POST['submit_btn']
		key = request.POST['key']

		is_save_file = request.POST.get('is_save_file', False)

		form = UploadFileForm(request.POST, request.FILES)

		filename = str(form['upload'].value())
		filepath = os.path.join(settings.MEDIA_ROOT, filename)

		result = None

		if form.is_valid() and filename != 'None':
			if submit_btn == 'encrypt':
				if key:
					fs = FileSystemStorage()
					if filename not in os.listdir(settings.MEDIA_ROOT):
						fs.save(filename, request.FILES['upload'])
					content = rc4.read_file_as_bytes(filepath)
					encrypted_content = rc4.encrypt(content, key.encode())
					rc4.write_file_in_bytes(filepath, encrypted_content)
					context['key'] = key
					context['success'] = 'File encrypted.'
				else:
					messages.info(request, 'Encrypting file requires key.')
			else:
				if key:
					content = rc4.read_file_as_bytes(filepath)
					decrypted_content = rc4.decrypt(content, key.encode())
					rc4.write_file_in_bytes(filepath, decrypted_content)
					context['key'] = key
					context['success'] = 'File decrypted.'
				else:
					messages.info(request, 'Decrypting file requires key.')

		if plain_text:
			if key:
				if submit_btn == 'encrypt':
					plain_content = rc4.encrypt(plain_text.encode(), key.encode(), toBase64=True)
					result = plain_content
				else:
					plain_content = rc4.decrypt(plain_text.encode(), key.encode(), fromBase64=True)
					result = plain_content.decode()

				if is_save_file:
					if type(plain_content) == str:
						plain_content = plain_content.encode()
					save_to_path = os.path.join(settings.MEDIA_ROOT, 'ciphertext.txt')
					rc4.write_file_in_bytes(save_to_path, plain_content)

				context['plain_text'] = plain_text
				context['result'] = result
				context['key'] = key

			else:
				messages.info(request, 'Encrypting and decrypting text requires key.')

	return render(request, '02_stream_cipher.html', context)