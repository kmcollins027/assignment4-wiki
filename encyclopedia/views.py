from pickletools import read_uint1
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage


from . import util

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
    return render(request, "encyclopedia/create_page.html")

def edit_page(request, title):
    entry = title
    contents = util.get_entry(entry)
    context = {"entry": entry, "contents": contents}
    return render(request, "encyclopedia/edit_page.html", context)
    

def create(request):

    if request.method == "POST":
        TITLE = request.POST["create_entry_name"]
        content = request.POST["content"]
        util.save_entry(TITLE, content)
        entry_name = TITLE
        MD_to_HTML = md.convert(content)
        context = {"entry_name": entry_name, "entry_contents": MD_to_HTML}
        return render(request, "encyclopedia/show_entry.html", context)
