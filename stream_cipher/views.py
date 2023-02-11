from django.shortcuts import render

# Create your views here.
def stream_cipher(request):
	return render(request, '02_stream_cipher.html')