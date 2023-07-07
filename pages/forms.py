from django import forms
from managers.models import Manager
from listings.models import RealtyType
from django.db.models import Count
from django.utils.translation import gettext_lazy as _


class SearchManager(forms.Form):
    manager = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                     empty_label=_("Full name"),
                                     queryset=Manager.objects.all().order_by('full_name'))
    
    class Meta:
        fields = '__all__'


class SellerForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
                            attrs={
                                'placeholder': "",
                                'class': 'input input_secondary'
                            }))
    realty_type = forms.ModelChoiceField(
        label=_("Realty type"),
        queryset=RealtyType.objects.annotate(listing_count=Count('listings')).filter(listing_count__gt=0)
                .order_by('title'),
        empty_label=_("Select type"),
        required=False,
        widget=forms.Select(attrs={
            'class': 'select', 'data-prefix': _("Realty type:")
            })
    )
    class Meta:
        fields = '__all__'
