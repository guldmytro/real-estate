from news.models import PostModel
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Analytic(PostModel):
    class Meta:
        verbose_name = _('Analytical review')
        verbose_name_plural = _('Analytical reviews')

    def get_absolute_url(self):
        return reverse('analytics:detail', kwargs={'slug': self.slug})    