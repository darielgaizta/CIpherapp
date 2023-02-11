from django.urls import path
from . import views

urlpatterns = [
	path('', views.stream_cipher, name='stream_cipher')
]