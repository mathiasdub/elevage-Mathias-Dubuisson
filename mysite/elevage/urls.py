from django.urls import path
from . import views


app_name = "elevage"
urlpatterns = [
    path("nouveau/", views.nouveau, name="nouveau"),
]