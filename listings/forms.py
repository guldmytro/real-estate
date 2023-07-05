from django import forms
from .models import RealtyType, Kit, Deal
from django.db.models import Count

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
        label="Тип угоди",
        queryset=Deal.objects.annotate(listing_count=Count('listings')).filter(listing_count__gt=0),
        required=False,
        widget=forms.widgets.RadioSelect(attrs={'class': 'radio', 'data-prefix': 'Тип угоди:'})
    )
    address_input = forms.CharField(label='Адреса', required=False, 
                                    widget=forms.widgets.TextInput(
                                        attrs={
                                           'class': 'input',
                                           'placeholder': 'Наприклад, Харків, Сумська...',
                                           'autocomplete': 'off'
                                        })
                                    )
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
        queryset=RealtyType.objects.annotate(listing_count=Count('listings')).filter(listing_count__gt=0)
        .order_by('title'),
        empty_label='Виберіть тип',
        required=False,
        widget=forms.Select(attrs={
            'class': 'select', 'data-prefix': "Тип об'єкту:"
            })
    )

    # Popular fields
    is_new_building = forms.BooleanField(
        label='Новобудова',
        required=False,
        widget=forms.CheckboxInput(attrs={'data-label': 'Новобудова'})
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
            .filter(listing_count__gt=0).order_by('value'),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Ремонт:'})
    )

    planning = forms.ModelChoiceField(
        label='Планування',
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['planning'])
        .annotate(listing_count=Count('listing'))
        .filter(listing_count__gt=0).order_by('value'),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Планування:'})
    )

    listing_class = forms.ModelChoiceField(
        label='Клас оселі',
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['listing_class'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0).order_by('value'),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Клас оселі:'})
    )

    floor = forms.ModelChoiceField(
        label='Перекриття',
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['floor'])
        .annotate(listing_count=Count('listing'))
        .filter(listing_count__gt=0).order_by('value'),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Перекриття:'})
    )

    windows = forms.ModelChoiceField(
        label='Вікна виходять',
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['windows'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0).order_by('value'),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': 'Вікна виходять:'})
    )

    # Outside
    enter = forms.ModelChoiceField(
        label="Під'їзд / вхід",
        queryset=Kit.objects.filter(attribute__slug=FILTER_PROPS['enter'])
            .annotate(listing_count=Count('listing'))
            .filter(listing_count__gt=0).order_by('value'),
        empty_label='Вибрати',
        required=False,
        widget=forms.Select(attrs={'class': 'select', 'data-prefix': "Під'їзд / вхід:"})
    )

    class Meta:
        fields = '__all__'


class SearchFormSimplified(SearchForm):
    class Meta:
        fields = ['address_input', 'city', 'street']
