from django.urls import path
from . import views


app_name = "elevage"
urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("nouveau/", views.nouveau, name="nouveau"),
    path("liste/", views.liste, name="liste"),
    path("elevage/<int:elevage_id>/", views.detail, name="detail"),
]