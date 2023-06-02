from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        pass
