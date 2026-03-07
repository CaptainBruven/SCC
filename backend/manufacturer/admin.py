from django.contrib import admin

from manufacturer.models import Manufacturer


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "manufacturer_type", "species", "is_alien")
    list_filter = ("manufacturer_type", "is_alien", "species")
    search_fields = ("name", "code", "slug")
    prepopulated_fields = {"slug": ("name",)}
