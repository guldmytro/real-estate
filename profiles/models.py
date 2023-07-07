from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class AdvUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
