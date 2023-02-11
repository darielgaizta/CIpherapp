from django import forms

class UploadFileForm(forms.Form):
	upload = forms.FileField(required=False, widget=forms.FileInput(attrs={
		'id': 'file-upload',
		'class': 'form-control',
		}))