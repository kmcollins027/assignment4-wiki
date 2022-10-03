from socket import fromshare
from django import forms 

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Contents", widget=forms.Textarea)


class EditForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
