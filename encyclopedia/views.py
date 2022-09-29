from django.shortcuts import render
from django.core.files.storage import default_storage


from . import util

import markdown2

md = markdown2.Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, TITLE):
    entry_name = TITLE
    html_contents = util.get_entry(entry_name)
    if html_contents is None:
        return render(request, "encyclopedia/index.html", {"errormsg": "Requested page not found"})
    else:
        MD_to_HTML = md.convert(html_contents)
        return render(request, "encyclopedia/show_entry.html", {"entry_contents": MD_to_HTML, "entry_name": entry_name})

def create_page(request):
    entry = request.GET["entry_name"]
    text_contents = request.GET["contents"]

    if default_storage.exists(entry):
        render(request, "encyclopedia.index.html", {"errmsg": "Page already exists"})
    else:
        util.save_entry(entry, text_contents)
        html_contents = util.get_entry(entry)
        MD_to_HTML = md.convert(html_contents)
        render(request, "encyclopedia/show_entry.html", {"entry_contents": MD_to_HTML, "entry_name": entry})

