from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

from PIL import Image

MIN_RESOLUTION = (100, 100)
MAX_RESOLUTION = (1000, 1000)
MAX_IMAGE_SIZE = 4000000


class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; font-size:14px;">Загружайте информацию с минимальным разрешением {}x{}</span>'.format(
                *self.MIN_RESOLUTION)
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if max_height < img.height < min_height or max_width < img.width < min_width:
            raise ValidationError('Разрешение не подходит')
        if image.size > MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен привешать 3 МБ')
        return image


class NotebookAdmin(admin.ModelAdmin):
    """При создании товара в графе 'категория' видна только 'ноутбуки'"""

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    """При создании товара в графе 'категория' видна только для 'смартфоны'"""

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(SomeModel)
