from django import forms

class UploadFaturaForm(forms.Form):
    arquivo = forms.FileField()