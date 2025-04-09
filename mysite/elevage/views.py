from django.shortcuts import render, get_object_or_404
from .models import Elevage


def nouveau(request):
    return render(request, "elevage/nouveau.html")


def liste(request):
    return render(request, "elevage/liste.html")


def detail(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)
    return render(request, "elevage/detail.html", {"elevage" : elevage})