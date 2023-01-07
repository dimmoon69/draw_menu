from django.db import models

from backend.menubar.utils import slugify


class Menu(models.Model):

    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.CharField('Ссылка', max_length=250, blank=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = f'/{slugify(self.name)}'
        super(Menu, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class MenuItem(models.Model):

    menu = models.ForeignKey(Menu, verbose_name='Меню', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=150, unique=True)
    slug = models.CharField('Ссылка', max_length=250, blank=True, editable=False)
    parent = models.ForeignKey(
        'self',
        verbose_name='Родитель',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        obj = self.__class__.objects.filter(name=self.parent).first()
        slug = obj.slug if obj and self.parent is not None else self.menu.slug
        self.slug = f'{slug}/{slugify(self.name)}'
        super(MenuItem, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

