from pickletools import read_uint1
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
from django.contrib import messages 

import random 

from . import util, forms

import markdown2

md = markdown2.Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki_entry(request, title):
    entries = util.list_entries()
    entry_name = title
    contents = util.get_entry(entry_name)
    if contents is None:
        return render("encyclopedia/index.html", {"entries": entries, "msg": "Requested page not found"})
    else:
        MD_to_HTML = md.convert(contents)
        return render(request, "encyclopedia/show_entry.html", {"entry_contents": MD_to_HTML, "entry_name": entry_name})



def create_page(request):
    if request.method == "POST":
        form = forms.CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/create_page.html", {"form": form, "msg": "Entry already exists. Please enter a unique entry."})
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

def random_page(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki_entry", args=[entry]))

def search(request):
    entry_list = util.list_entries()
    if request.method == "POST":
        search = request.POST.get("q")
        if search is not None:
            search = search.lower().strip()
            for entry in entry_list:
                if search == entry.lower():
                    title = entry
                    return HttpResponseRedirect(reverse("wiki_entry", args=[title]))
                else:
                    if search in entry.lower():
                        entry_list = list(filter(lambda x: search in x.lower(), entry_list))
                        return render(request, "encyclopedia/msg_page.html", {"search": search, "entry_list": entry_list})
            entry_list = list(filter(lambda x: search in x.lower(), entry_list))
            if not entry_list:
                return render(request, "encyclopedia/msg_page.html", {"notFound": "Entry doesn't exist"})

def delete_entry(request, title):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)

    msg = f'{title} entry was successfully deleted'
    messages.success(request, msg)
    return redirect(index)