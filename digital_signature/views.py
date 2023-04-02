from django.shortcuts import render

# Create your views here.
def digital_signature(request):
    return render(request, '03_digital_signature.html')