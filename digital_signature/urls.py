from django.urls import path

from . import views

urlpatterns = [
    path('', views.digital_signature, name='digital_signature')
]
