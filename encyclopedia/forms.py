from mimetypes import init
from socket import fromshare
from django import forms 
from . import util, views

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Contents", widget=forms.Textarea)


class EditForm(forms.Form):
    title = forms.CharField(label="")
    content = forms.CharField(label="", widget=forms.Textarea)

