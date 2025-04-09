from django.shortcuts import render, get_object_or_404, redirect
from .models import Elevage
from .forms import ElevageForm


def menu(request):
    return render(request, "elevage/menu.html")


def nouveau(request):
    if request.method == 'POST':
        form = ElevageForm(request.POST)
        if form.is_valid():
            elevage = form.save()
            return redirect('elevage:elevage/', elevage_id=elevage.id)  
    else:
        form = ElevageForm()
    return render(request, 'elevage/nouveau.html', {'form': form})


def liste(request):
    return render(request, "elevage/liste.html")


def detail(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)
    return render(request, "elevage/detail.html", {"elevage" : elevage})