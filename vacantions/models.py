from django.db import models


class Vacantion(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    salary = models.CharField(max_length=30, verbose_name='Зарплата')
    description = models.TextField(max_length=500, verbose_name='Опис')
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Вакансія'
        verbose_name_plural = 'Вакансії'


class Department(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок', unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)
        verbose_name = 'Відділ'
        verbose_name_plural = 'Відділи'
