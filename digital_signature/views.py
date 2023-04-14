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
        p = int(request.POST['p'])
        q = int(request.POST['q'])
        context['p'] = p
        context['q'] = q

        # Get RSA key
        private_key, public_key = generate_rsa_key(p, q)
        context['encryption_key'] = private_key[0]
        context['decryption_key'] = public_key[0]
        
        form = UploadFileForm(request.POST, request.FILES)

        filename = str(form['upload'].value())
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        parameter_filepath = os.path.join(settings.MEDIA_ROOT, 'params.txt')
        
        idx = filename.index('.')
        signature_filepath = os.path.join(settings.MEDIA_ROOT, f'signature_{filename[:idx]}.txt')

        if form.is_valid() and filename != 'None':
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
                    if filename.endswith('.txt'):
                        new_content = content + signature.encode('utf-8')
                        write_file_in_bytes(filepath, new_content)
                    else:
                        write_file_in_bytes(signature_filepath, signature.encode('utf-8'))

                    current_params = f'''
                        Encryption key: {private_key[0]}
                        Decryption key: {public_key[0]}
                        p: {p}
                        q: {q}
                    '''
                    write_file_in_bytes(parameter_filepath, current_params.encode())

                    context['message_pos'] = 'File SIGNED SUCCESSFULLY'  
                else:
                    messages.info(request, 'Private key is not provided.')    
            else:
                # Verify signature
                if public_key:
                    content = read_file_in_bytes(filepath)
                    if filename.endswith('.txt'):
                        content, signature = scan_content(content)
                    else:
                        signature = read_file_in_bytes(signature_filepath)
                    if signature:
                        hashed_content = hash_message(encoded_string=content)
                        status = verify_signature(hashed_content, signature, public_key)

                        if status:
                            context['message_pos'] = 'File is OK.'
                        else:
                            context['message_neg'] = 'File is NOT AUTHENTIC.'
                    else:
                        messages.info(request, 'Signature not found.')
                else:
                    messages.info(request, 'Public key is not provided.')

    return render(request, '03_digital_signature.html', context)