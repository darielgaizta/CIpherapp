from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from .forms import UploadFileForm
from .utils.digital_signature import *

import os

# Create your views here.
def digital_signature(request):
    context = {
        'form': UploadFileForm()
    }

    if request.method == 'POST':
        submit_btn = request.POST.get('submit_btn', False)
        p = int(request.POST['public_key'])
        q = int(request.POST['private_key'])

        private_key, public_key = generate_rsa_key(p, q)
        
        form = UploadFileForm(request.POST, request.FILES)

        filename = str(form['upload'].value())
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        if form.is_valid() and filename != 'None':
            context['p'] = p
            context['q'] = q
            if submit_btn == 'sign':
                # Sign signature
                if private_key:
                    fs = FileSystemStorage()
                    if filename not in os.listdir(settings.MEDIA_ROOT):
                        fs.save(filename, request.FILES['upload'])
                    content = read_file_in_bytes(filepath)
                    
                    # Get signature
                    hashed_content = hash_message(content)
                    signature = sign_digital_signature(hashed_content, private_key)
                    
                    # Write signature to file
                    new_content = content + signature.encode('utf-8')
                    write_file_in_bytes(filepath, new_content)

                    context['message_pos'] = 'File signed successfully'  
                else:
                    messages.info(request, 'Private key is not provided.')    
            else:
                # Verify signature
                if public_key:
                    content = read_file_in_bytes(filepath)
                    content, signature = scan_content(content)
                    hashed_content = hash_message(encoded_string=content)
                    status = verify_signature(hashed_content, signature, public_key)

                    if status:
                        context['message_pos'] = 'File is authentic.'
                    else:
                        context['message_neg'] = 'File is not authentic.'
                else:
                    messages.info(request, 'Public key is not provided.')

    return render(request, '03_digital_signature.html', context)