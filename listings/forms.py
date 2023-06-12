from django import forms


class SearchForm(forms.Form):
    address_input = forms.CharField(label='Address', required=False, 
                                   widget=forms.widgets.TextInput(
                                       attrs={
                                           'class': 'input',
                                           'placeholder': 'Enter the city, street...',
                                           'autocomplete': 'off'
                                           }))
    city = forms.CharField(required=False, widget=forms.widgets.HiddenInput)
    street = forms.CharField(required=False, widget=forms.widgets.HiddenInput)

    class Meta:
        fields = ('address_input', 'city', 'street')