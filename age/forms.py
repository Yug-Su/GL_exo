from django import forms

class DateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'datePicker'}),
        label="Sélectionnez une date :"  # Label plus clair
    )