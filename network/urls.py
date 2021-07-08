
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all", views.all, name='all'),
    path("user/<int:user_id>", views.profile, name='profile'),
    path('post/like', views.like, name='like'),
    path('post/edit', views.edit, name='edit')
]
