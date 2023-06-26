from django import forms


class SearchForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Введіть Прізвище ім'я фахівця"
    }))

    class Meta:
        fields = '__all__'
        