from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
