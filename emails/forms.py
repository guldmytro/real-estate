from django import forms


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