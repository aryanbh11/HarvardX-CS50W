from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("random_page", views.random_page, name="random"),
    path("create_page", views.create_page, name="create"),
    path("search_results", views.search_results, name="search"),
    path("wiki/<str:title>", views.page, name="page"),
    path("edit_page/<str:title>", views.edit_page, name="edit")
]
