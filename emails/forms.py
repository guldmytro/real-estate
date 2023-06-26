from django import forms
from vacantions.models import Vacantion
from managers.models import Review, Manager


class FeadbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                           attrs={
                               'placeholder': "Ваше ім'я:*",
                               'class': 'input input_secondary'
                           }))
    phone = forms.CharField(widget=forms.TextInput(
                            attrs={
                                'placeholder': "Телефон:*",
                                'class': 'input input_secondary'
                            }))
    
    class Meta:
        fields = '__all__'


class ApplyForm(FeadbackForm):
    file = forms.FileField()
    vacantion = forms.ModelChoiceField(label='Резюме',
                                       queryset=Vacantion.objects.all(),
                                       widget=forms.HiddenInput())
    

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'rating__star'}), 
                               choices=Review.RATING_CHOICES, initial=5)
    author = forms.CharField(widget=forms.TextInput(
                             attrs={
                                 'placeholder': "Ваше ім'я:*",
                                 'class': 'input'
                             }))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea',
                                                           'placeholder': 'Напишіть ваш відгук'}))
    phone = forms.CharField(widget=forms.TextInput(
                            attrs={
                                'placeholder': "Телефон:*",
                                'class': 'input'
                            }))
    manager = forms.ModelChoiceField(widget=forms.HiddenInput,
                                     queryset=Manager.objects.all())

    class Meta:
        model = Review
        fields = '__all__'
