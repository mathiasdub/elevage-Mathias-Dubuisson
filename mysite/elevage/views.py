from django.shortcuts import render
from django.http import HttpResponse


def nouveau(request):
    return render(request, "elevage/nouveau.html")


def liste(request):
    return render(request, "elevage/liste.html")