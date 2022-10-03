from mimetypes import init
from socket import fromshare
from django import forms 

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Contents", widget=forms.Textarea)


class EditForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)

