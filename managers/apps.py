from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManagersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'managers'
    verbose_name = _('Managers')
