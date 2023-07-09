from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class Vacantion(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=255, verbose_name=_('Title')),
        salary = models.CharField(max_length=30, verbose_name=_('Salary')),
        description = models.TextField(max_length=500, verbose_name=_('Description')),
    )
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name=_('Department'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created',)
        verbose_name = _('Vacancy')
        verbose_name_plural = _('Vacancies')


class Department(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=100, verbose_name=_('Title'), unique=True),
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
