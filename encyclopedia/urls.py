from django.urls import path, re_path

from . import views

#app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create_page/", views.create_page, name="create_page"),
    path("wiki/random/", views.random_page, name="random"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/delete/<str:title>/", views.delete_entry, name="delete"),
    path("wiki/edit_page/<str:title>/", views.edit_page, name="edit_page"),
    path("wiki/<str:title>/", views.wiki_entry, name="wiki_entry"),
]
