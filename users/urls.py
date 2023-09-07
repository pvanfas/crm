from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("set-user-timezone/", views.set_user_timezone, name="set_user_timezone"),
]
