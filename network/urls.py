
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("users/<str:username>", views.users, name="users"),
    path("following", views.following, name="following"),

    # API routes
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.like, name="like")
]
