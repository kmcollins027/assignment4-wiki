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
        return render(request, "encyclopedia/index.html", {"errormsg": "Requested page not found"})
    else:
        MD_to_HTML = md.convert(contents)
        return render(request, "encyclopedia/show_entry.html", {"entry_contents": MD_to_HTML, "entry_name": entry_name})



def create_page(request):
    return render(request, "encyclopedia/create_page.html")

def edit_page(request):
    return render(request, "encyclopedia/edit_page.html")
    

def create_or_edit(request):

    if request.method == "POST":
        #TITLE = request.POST.get("create_entry_name", "").strip()
        TITLE = request.POST["create_entry_name"]
        #content = request.POST.get("content", "").strip()
        content = request.POST["content"]
        util.save_entry(TITLE, content)
        entry_name = TITLE
        MD_to_HTML = md.convert(content)
        context = {"entry_name": entry_name, "entry_contents": MD_to_HTML}
        return render(request, "encyclopedia/show_entry.html", context)
        #return redirect("encyclopedia/show_entry.html", TITLE=TITLE)

    
    #html_contents = util.get_entry(entry)
    #MD_to_HTML = md.convert(html_contents)
  
    

    #entry = request.GET["entry_name"]
    #text_contents = request.GET["contents"]

    #if default_storage.exists(entry):
        #render(request, "encyclopedia.index.html", {"errmsg": "Page already exists"})
    #else:
        #util.save_entry(entry, text_contents)
        #html_contents = util.get_entry(entry)
        #MD_to_HTML = md.convert(html_contents)
        #render(request, "encyclopedia/show_entry.html", {"entry_contents": MD_to_HTML, "entry_name": entry})

