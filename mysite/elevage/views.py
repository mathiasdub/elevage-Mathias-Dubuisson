from django.shortcuts import render, get_object_or_404, redirect
from .models import Elevage
from .forms import ElevageForm, IndividuFormSet


def menu(request):
    return render(request, "elevage/menu.html")


def nouveau(request):
    if request.method == 'POST':
        elevage_form = ElevageForm(request.POST)
        formset = IndividuFormSet(request.POST)

        if elevage_form.is_valid() and formset.is_valid():
            elevage = elevage_form.save()
            individus = formset.save(commit=False)
            for individu in individus:
                individu.elevage = elevage
                individu.save()
            return redirect('elevage:liste')
    else:
        elevage_form = ElevageForm()
        formset = IndividuFormSet()

    return render(request, 'elevage/nouveau.html', {
        'elevage_form': elevage_form,
        'formset': formset,
    })


def liste(request):
    elevages = Elevage.objects.all()
    return render(request, "elevage/liste.html", {"elevages" : elevages})


def detail(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)
    return render(request, "elevage/detail.html", {"elevage" : elevage})