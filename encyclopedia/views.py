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
            if title in util.list_entries():
                return render(request, "encyclopedia/error_page.html", {"errormsg": "Entry already exists.."})
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(wiki_entry, title=title)
        else:
            return render(request, "encyclopedia/create_page.html", {"form": form})
    return render(request, "encyclopedia/create_page.html", {"form": forms.CreateForm()})


def edit_page(request, title):
    if request.method == "POST":
        form = forms.EditForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title, new_content)
            return redirect(wiki_entry, title=title)

    else:
        contents = util.get_entry(title)
        edit_form = forms.EditForm(initial={"title": title, "content": contents})
        return render(request, "encyclopedia/edit_page.html", {"edit_form": edit_form, "entry": title})

    #return render(request, "encyclopedia/edit_page.html", {"edit_form": forms.EditForm(), "entry": title})

