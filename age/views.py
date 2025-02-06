from django.shortcuts import render, redirect
from .forms import DateForm
from datetime import date
from django.http import Http404, HttpResponse

# Create your views here.

def index(request):

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            date_user = form.cleaned_data['date']
            date_now = date.today()
            diff = date_now - date_user

            # Extraction des années, mois, jours
            years = diff.days // 365
            months = (diff.days % 365) // 30  # Approximation des mois
            days = (diff.days % 365) % 30

            # Calcul des secondes (approximation)
            seconds = diff.days * 24 * 3600 + diff.seconds
            if years >=0:
                return render(request, 'index.html', {'form': form, 'diff': diff, 'years': years, 'months': months, 'days': days, 'seconds': seconds})
            else:
                raise Http404("Date de naissance invalide")  # Ou une autre exception appropriée
    else:
        form = DateForm()
    return render(request, 'index.html', {'form': form})