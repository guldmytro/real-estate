from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VacantionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vacantions'
    verbose_name = _('Vacancies')