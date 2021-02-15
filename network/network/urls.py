
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("api/compose", views.compose, name="compose"),
    path("api/posts/<int:type>/<str:username>", views.get_posts, name="posts"),
    path("api/post/<int:id>", views.get_post, name="single_post"),
    path("api/profiles/<str:username>", views.get_profile, name="profiles"),
    path("api/is_following/<str:username_1>/<str:username_2>", views.is_following, name="is_following"),
    path("api/likes/<str:username>/<int:post_id>", views.likes, name="likes")
]
