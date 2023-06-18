from django import forms
from .models import RealtyType, Kit
from django.db.models import Count

FILTER_PROPS = {
    'repair': 'property_18',
    'lift': 'property_100',
    'parking': 'property_101',
    'outside_decorating': 'property_102'
}

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
        widget=forms.widgets.RadioSelect(attrs={'class': 'radio', 'data-prefix': 'Кімнатність:'})
    )
    min_price = forms.IntegerField(
        label='Мінімальна ціна',
        required=False,
        widget=forms.widgets.NumberInput(attrs={
            'class': 'input-price', 'placeholder': 'Від',
            'data-prefix': 'Ціна від', 'data-suffix': "$"})
    )
    max_price = forms.IntegerField(
        label='Максимальна ціна',
        required=False,
        widget=forms.widgets.NumberInput(attrs={
            'class': 'input-price', 'placeholder': 'До',
            'data-prefix': 'Ціна до', 'data-suffix': "$"})
    )
    realty_type = forms.ModelChoiceField(
        label="Тип об'єкту",
        queryset=RealtyType.objects.annotate(listing_count=Count('listings')).filter(listing_count__gt=0),
        empty_label='Виберіть тип',
        required=False,
        widget=forms.Select(attrs={
            'class': 'select', 'data-prefix': "Тип об'єкту:"
            })
    )

    # Popular fields
    is_new_building = forms.BooleanField(
        label='Новий дім',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox',
                                          'data-label': 'Новий дім'})
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
        label='З фото',
        required=False,
        widget=forms.CheckboxInput(attrs={'data-label': 'З фото'})
    )
    with_video = forms.BooleanField(
        label='З відео',
        required=False,
        widget=forms.CheckboxInput(attrs={'data-label': 'З відео'})
    )

    # House
    floor_from = forms.IntegerField(
        label='Від',
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 
                                                'placeholder': 'Від',
                                                'data-prefix': 'Поверх від'})
    )
    floor_to = forms.IntegerField(
        label='До',
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 
                                                'placeholder': 'До',
                                                'data-prefix': 'Поверх до'})
    )
    floors_from = forms.IntegerField(
        label='Від',
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 
                                                'placeholder': 'Від',
                                                'data-prefix': 'Поверхів у домі від'})
    )
    floors_to = forms.IntegerField(
        label='До',
        required=False,
        widget=forms.widgets.NumberInput(attrs={'class': 'input-price', 
                                                'placeholder': 'До',
                                                'data-prefix': 'Поверхів у домі до'})
    )
    repair = forms.ModelChoiceField(
        label='Ремонт',
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['repair'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Ремонт:'})
    )
    lift = forms.ModelChoiceField(
        label='Ліфт',
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['lift'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Ліфт:'})
    )

    # Outside
    parking = forms.ModelChoiceField(
        label='Парковка',
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['parking'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Парковка:'})
    )
    outside_decorating = forms.ModelChoiceField(
        label='Благоустрій двору',
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['outside_decorating'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Благоустрій двору:'})
    )

    class Meta:
        fields = '__all__'
