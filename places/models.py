from django.db import models
from tinymce import models as tinymce_models


# Create your models here.


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок",)
    description_long = tinymce_models.HTMLField(
        verbose_name="Длинное описание",
    )
    description_short = models.TextField(
        verbose_name="Короткое описание",
        null=True
    )
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    order = models.PositiveSmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Позиция",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta():
        ordering = ['order']


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        null=True,
        related_name="images",
        verbose_name="Место",
    )

    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="images",
    )

    order = models.PositiveSmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Позиция",
    )

    def __str__(self) -> str:
        return f"{self.place.title}"

    class Meta():
        ordering = ['order']
