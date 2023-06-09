from django import forms
from vacantions.models import Vacantion
from managers.models import Review, Manager
from django.utils.translation import gettext_lazy as _


class FeadbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                           attrs={
                               'placeholder': _("Your name:*"),
                               'class': 'input input_secondary'
                           }))
    phone = forms.CharField(widget=forms.TextInput(
                            attrs={
                                'placeholder': _("Phone:*"),
                                'class': 'input input_secondary'
                            }))
    
    class Meta:
        fields = '__all__'


class ApplyForm(FeadbackForm):
    file = forms.FileField()
    vacantion = forms.ModelChoiceField(label=_('Resume'),
                                       queryset=Vacantion.objects.all(),
                                       widget=forms.HiddenInput())
    

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'rating__star'}), 
                               choices=Review.RATING_CHOICES, initial=5)
    author = forms.CharField(widget=forms.TextInput(
                             attrs={
                                 'placeholder': _("Your name:*"),
                                 'class': 'input'
                             }))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea',
                                                        'placeholder': _("Write your review")}))
    phone = forms.CharField(widget=forms.TextInput(
                            attrs={
                                'placeholder': _("Phone:*"),
                                'class': 'input'
                            }))
    manager = forms.ModelChoiceField(widget=forms.HiddenInput,
                                     queryset=Manager.objects.all())

    class Meta:
        model = Review
        fields = '__all__'


class ListingPhoneForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
                        attrs={
                            'placeholder': _("Phone:*"),
                            'class': 'input'
                        }))
    
    class Meta:
        fields = '__all__'


class ListingMessageForm(ListingPhoneForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'textarea', 'placeholder': _("Message")}
            )
        )


class ListingVisitForm(ListingPhoneForm):
    date = forms.DateField(widget=forms.TextInput(
        attrs={'type': 'date', 'class': 'input'}
    ))
    time = forms.TimeField(widget=forms.TextInput(
        attrs={'type': 'time', 'class': 'input'}
    ))

