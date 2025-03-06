
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name ="profile"),
    path("following", views.following_view, name="following"),
    
    #API ROUTES
    path("thread/<int:thread_id>", views.thread_view, name="thread_api"), 
    path("user_api/<int:user_id>", views.user_api, name="user_api"),
    path("edit_api/<int:thread_id>", views.edit_api, name="edit_api")
]
