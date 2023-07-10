from django import forms
from .models import RealtyType, Kit, Deal
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

FILTER_PROPS = {
    'repair': 'property_18',
    'planning': 'property_20',
    'listing_class': 'property_21',
    'windows': 'property_25',
    'floor': 'property_28',
    'enter': 'property_29',
}


class SearchForm(forms.Form):
    deal = forms.ModelChoiceField(
        label=_('Type of agreement'),
        queryset=Deal.objects.annotate(listing_count=Count('listings')).filter(listing_count__gt=0),
        required=False,
        widget=forms.widgets.RadioSelect(attrs={'class': 'radio', 'data-prefix': _('Type of agreement:')})
    )
    address_input = forms.CharField(label=_('Address'), required=False, 
                                    widget=forms.widgets.TextInput(
                                        attrs={
                                           'class': 'input',
                                           'placeholder': _('For example, Kharkiv'),
                                           'autocomplete': 'off'
                                        })
                                    )
    city = forms.CharField(required=False, widget=forms.widgets.HiddenInput)
    street = forms.CharField(required=False, widget=forms.widgets.HiddenInput)
    number_of_rooms = forms.ChoiceField(
        label=_('Rooms'),
        required=False,
        choices=(
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4+', '4+')
        ),
        widget=forms.widgets.RadioSelect(attrs={'class': 'radio', 'data-prefix': _('Rooms:')})
    )
    min_price = forms.IntegerField(
        label=_('Minimum price'),
        required=False,
        widget=forms.widgets.NumberInput(attrs={
            'class': 'input-price', 'placeholder': _('From'),
            'data-prefix': _('Price from:'), 'data-suffix': "$"})
    )
    max_price = forms.IntegerField(
        label=_('Maximum price'),
        required=False,
        widget=forms.widgets.NumberInput(attrs={
            'class': 'input-price', 'placeholder': _('To'),
            'data-prefix': _('Price to:'), 'data-suffix': "$"})
    )
    realty_type = forms.ModelChoiceField(
        label=_("Realty type"),
        queryset=RealtyType.objects.annotate(listing_count=Count('listings')).filter(listing_count__gt=0)
        .order_by('title'),
        empty_label=_('Select a type'),
        required=False,
        widget=forms.Select(attrs={
            'class': 'select', 'data-prefix': _("Realty type:")
            })
    )

    # Popular fields
    is_new_building = forms.BooleanField(
        label=_('New building'),
        required=False,
        widget=forms.CheckboxInput(attrs={'data-label': _('New building')})
    )
    animals = forms.BooleanField(
        label='Можна з тваринами',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox',
                                          'data-label': 'Можна з тваринами'})
    )
    furniture = forms.BooleanField(
        label='З меблями',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox',
                                          'data-label': 'З меблями'})
    )
    for_students = forms.BooleanField(
        label='Для студентів',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox',
                                          'data-label': 'Для студентів'})
    )
    conditioner = forms.BooleanField(
        label='Є кондиціонер',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox',
                                          'data-label': 'Є кондиціонер'})
    )
    without_furniture = forms.BooleanField(
        label='Без меблів',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox',
                                          'data-label': 'Без меблів'})
    )

    # Media
    with_photo = forms.BooleanField(
        label=_('With photo'),
        required=False,
        widget=forms.CheckboxInput(attrs={'data-label': _('With photo')})
    )
    with_video = forms.BooleanField(
        label=_('With video'),
        required=False,
        widget=forms.CheckboxInput(attrs={'data-label': _('With video')})
    )

    # House
    floor_from = forms.IntegerField(
        label=_('From'),
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 
                                                'placeholder': _('From'),
                                                'data-prefix': _('Floor from:')})
    )
    floor_to = forms.IntegerField(
        label=_('To'),
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 
                                                'placeholder': _('To'),
                                                'data-prefix': _('Floor to:')})
    )
    floors_from = forms.IntegerField(
        label=_('From'),
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 
                                                'placeholder': _('From'),
                                                'data-prefix': _('Floors in the house from:')})
    )
    floors_to = forms.IntegerField(
        label=_('To'),
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 
                                                'placeholder': _('To'),
                                                'data-prefix': _('Floors in the house to:')})
    )
    repair = forms.ModelChoiceField(
        label=_('Repair'),
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['repair'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0).order_by('translations__value'),
        empty_label=_('Select'),
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': _('Repair:')})
    )

    planning = forms.ModelChoiceField(
        label=_('Layout'),
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['planning'])
        .annotate(listing_count=Count('listing'))
        .filter(listing_count__gt=0).order_by('translations__value'),
        empty_label=_('Select'),
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': _('Layout:')})
    )

    listing_class = forms.ModelChoiceField(
        label=_('Housing class'),
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['listing_class'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0).order_by('translations__value'),
        empty_label=_('Select'),
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': _('Housing class:')})
    )

    floor = forms.ModelChoiceField(
        label=_('Roof of the house'),
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['floor'])
        .annotate(listing_count=Count('listing'))
        .filter(listing_count__gt=0).order_by('translations__value'),
        empty_label=_('Select'),
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': _('Roof of the house:')})
    )

    windows = forms.ModelChoiceField(
        label=_('Windows come out'),
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['windows'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0).order_by('translations__value'),
        empty_label=_('Select'),
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': _('Windows come out:')})
    )

    # Outside
    enter = forms.ModelChoiceField(
        label=_('Entrance'),
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['enter'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0).order_by('translations__value'),
        empty_label=_('Select'),
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': _('Entrance:')})
    )

    class Meta:
        fields = '__all__'


class SearchFormSimplified(SearchForm):
    class Meta:
        fields = ['address_input', 'city', 'street']
