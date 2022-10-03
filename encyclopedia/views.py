from pickletools import read_uint1
from django.shortcuts import render, redirect
from http.client import HTTPResponse
from django.core.files.storage import default_storage



from . import util, forms

import markdown2

md = markdown2.Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki_entry(request, title):
    entry_name = title
    contents = util.get_entry(entry_name)
    if contents is None:
        return redirect("encyclopedia/error_page.html", {"errormsg": "Requested page not found"})
    else:
        MD_to_HTML = md.convert(contents)
        return render(request, "encyclopedia/show_entry.html", {"entry_contents": MD_to_HTML, "entry_name": entry_name})



def create_page(request):
    if request.method == "POST":
        form = forms.CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(wiki_entry, title=title)
        else:
            return render(request, "encyclopedia/create_page.html", {"form": form})
    return render(request, "encyclopedia/create_page.html", {"form": forms.CreateForm()})


def edit_page(request, title):
    entry = title
    contents = util.get_entry(entry)
    if request.method == "POST":
        edit_form = forms.EditForm(request.POST, instance=contents)
        if edit_form.is_valid():
            #title = edit_form.cleaned_data["title"]
            content = edit_form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(wiki_entry, title=title)
        else:
            return render(request, "encyclopedia/edit_page.html", {"edit_form": edit_form, "entry": entry})
    return render(request, "encyclopedia/edit_page.html", {"edit_form": forms.EditForm(), "entry": entry})
   # entry = title
    #contents = util.get_entry(entry)
    #context = {"entry": entry, "contents": contents}
   # return render(request, "encyclopedia/edit_page.html", context)
