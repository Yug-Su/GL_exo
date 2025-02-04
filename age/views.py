from django.shortcuts import render, redirect
from .forms import DateForm
from datetime import date

# Create your views here.

def index(request):

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            date_user = form.cleaned_data['date']
            date_now = date.today()
            diff_years = date_now.year - date_user.year

            return render(request, 'votre_template.html', {'diff_years': diff_years})
    else:
        form = DateForm()
    return render(request, 'index.html', {'form': form})