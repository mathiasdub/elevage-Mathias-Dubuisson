from django.shortcuts import render, get_object_or_404, redirect
from .models import Elevage, Individu
from .forms import ElevageForm, LapinForm, ChoixNombreLapinsForm
from django.forms import modelformset_factory



def menu(request):
    return render(request, "elevage/menu.html")


def nouveau(request):
    if 'nombre_lapins' not in request.session:
        if request.method == 'POST':
            choix_form = ChoixNombreLapinsForm(request.POST)
            if choix_form.is_valid():
                request.session['nombre_lapins'] = choix_form.cleaned_data['nombre_lapins']
                return redirect('elevage:nouveau')
        else:
            choix_form = ChoixNombreLapinsForm()
        return render(request, 'elevage/choix_nombre_lapins.html', {'form': choix_form})

    # Étape 2 : formulaire complet avec x lapins
    LapinFormSet = modelformset_factory(Individu, form=LapinForm, extra=request.session['nombre_lapins'])

    if request.method == 'POST':
        elevage_form = ElevageForm(request.POST)
        lapin_formset = LapinFormSet(request.POST, queryset=Individu.objects.none())
        if elevage_form.is_valid() and lapin_formset.is_valid():
            elevage = elevage_form.save()
            for form in lapin_formset:
                lapin = form.save(commit=False)
                lapin.elevage = elevage
                lapin.save()
            del request.session['nombre_lapins']
            return redirect('elevage:detail', elevage_id=elevage.id)
    else:
        elevage_form = ElevageForm()
        lapin_formset = LapinFormSet(queryset=Individu.objects.none())

    return render(request, 'elevage/nouveau.html', {
        'elevage_form': elevage_form,
        'lapin_formset': lapin_formset,
    })


def liste(request):
    elevages = Elevage.objects.all()
    return render(request, "elevage/liste.html", {"elevages" : elevages})


def detail(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)
    return render(request, "elevage/detail.html", {"elevage" : elevage})