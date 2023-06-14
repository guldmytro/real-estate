from django import forms
from .models import RealtyType
from django.db.models import Count


class SearchForm(forms.Form):
    address_input = forms.CharField(label='Адреса', required=False, 
                                   widget=forms.widgets.TextInput(
                                       attrs={
                                           'class': 'input',
                                           'placeholder': 'Наприклад, Львів, Полуботка...',
                                           'autocomplete': 'off'
                                           }))
    city = forms.CharField(required=False, widget=forms.widgets.HiddenInput)
    street = forms.CharField(required=False, widget=forms.widgets.HiddenInput)
    number_of_rooms = forms.ChoiceField(
        label='Кімнатність',
        required=False,
        choices=(
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4+', '4+')
        ),
        widget=forms.widgets.RadioSelect(attrs={'class': 'radio'})
    )
    min_price = forms.IntegerField(
        label='Мінімальна ціна',
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 'placeholder': 'Від'})
    )
    max_price = forms.IntegerField(
        label='Максимальна ціна',
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 'placeholder': 'До'})
    )
    realty_type = forms.ModelChoiceField(
        label='Realty Type',
        queryset=RealtyType.objects.annotate(listing_count=Count('listings')).filter(listing_count__gt=0),
        empty_label='Виберіть тип',
        required=False,
        widget=forms.Select(attrs={'class': 'select'})
    )

    class Meta:
        fields = (
            'address_input', 'city', 
            'street', 'number_of_rooms',
            'min_price', 'max_price',
            'realty_type')
