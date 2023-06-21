from django import forms
from vacantions.models import Vacantion


class FeadbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                           attrs={
                               'placeholder': "Ваше ім'я",
                               'class': 'input input_secondary'
                           }))
    phone = forms.CharField(widget=forms.TextInput(
                            attrs={
                                'placeholder': "Телефон",
                                'class': 'input input_secondary'
                            }))
    
    class Meta:
        fields = '__all__'


class ApplyForm(FeadbackForm):
    file = forms.FileField()
    vacantion = forms.ModelChoiceField(queryset=Vacantion.objects.all(),
                                       widget=forms.HiddenInput())
