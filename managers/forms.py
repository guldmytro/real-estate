from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': _('Enter the last name of the specialist')
    }))

    class Meta:
        fields = '__all__'
        