from django.shortcuts import render

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

