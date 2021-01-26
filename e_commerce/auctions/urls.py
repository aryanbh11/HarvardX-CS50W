from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing/<str:username>", views.create_listing, name="create_listing"),
    path("listings/<int:id>/<str:username>", views.display_listing, name="listings"),
    path("edit_watchlist/<int:id>/<str:username>", views.edit_watchlist, name="edit_watchlist"),
    path("watchlist/<str:username>", views.display_watchlist, name="watchlist"),
    path("categories/<str:name>", views.categories, name='categories'),
    path("close_listing/<int:id>/<str:username>", views.close_listing, name="close_listing"),
    path("add_comments/<int:id>/<str:username>", views.add_comment, name="comments")
]
