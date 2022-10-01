from django.urls import path, re_path

from . import views

#app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create_page/", views.create_page, name="create_page"),
    path("wiki/edit_page", views.edit_page, name="edit_page"),
    path("wiki/<str:title>/", views.wiki_entry, name="wiki_entry"),
    path("wiki/show_entry/", views.create_or_edit, name="create_update"),
    re_path(r"^wiki/(?P<title>).*[\s\w]*/$", views.wiki_entry, name="wiki_entry"),
    re_path(
        r"^update-entry/$",
        views.create_or_edit,
        name="create_update",
    ),
    re_path(
        r"^update-entry/?/(?P<title>.*\s*)/$",
        views.create_or_edit,
        name="create_update",
    ),
    
]
