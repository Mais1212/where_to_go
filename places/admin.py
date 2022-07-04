from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Place

# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    ordering = ["order"]


class ImageInline(SortableInlineAdminMixin, admin.StackedInline):
    def headshot_image(self, image):
        html = format_html(
            """<img src="{}" width="{}" height={} />""",
            image.image.url,
            200,
            200
        )

        return html

    headshot_image.short_description = 'Превью'
    model = Image
    readonly_fields = ["headshot_image"]
    fields = ("order", ("image",  "headshot_image"),)


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ["title", ]
