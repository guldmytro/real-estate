from django.db import models


class Document(models.Model):
    title = models.CharField(verbose_name='Заголовок')
    file = models.FileField(verbose_name='Файл', upload_to='documents/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'
