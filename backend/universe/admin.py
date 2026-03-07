from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from universe.models import (
    AsteroidBelt,
    CelestialBody,
    CelestialBodyBiome,
    JumpPoint,
    Location,
    Star,
    StarSystem,
)


class StarInline(TabularInline):
    model = Star
    extra = 0


class CelestialBodyInline(TabularInline):
    model = CelestialBody
    extra = 0
    fields = ("name", "body_type", "status")


class AsteroidBeltInline(TabularInline):
    model = AsteroidBelt
    extra = 0


@admin.register(StarSystem)
class StarSystemAdmin(ModelAdmin):
    list_display = ("name", "code", "status", "affiliation", "threat_level")
    list_filter = ("status", "affiliation", "threat_level")
    search_fields = ("name", "code", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [StarInline, CelestialBodyInline, AsteroidBeltInline]


@admin.register(Star)
class StarAdmin(ModelAdmin):
    list_display = ("name", "star_system", "star_type", "spectral_class")
    list_filter = ("star_type",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class CelestialBodyBiomeInline(TabularInline):
    model = CelestialBodyBiome
    extra = 0


class LocationInline(TabularInline):
    model = Location
    fk_name = "celestial_body"
    extra = 0
    fields = ("name", "location_type", "status")


@admin.register(CelestialBody)
class CelestialBodyAdmin(ModelAdmin):
    list_display = ("name", "star_system", "body_type", "habitable", "status")
    list_filter = ("body_type", "status", "habitable", "star_system")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CelestialBodyBiomeInline, LocationInline]


@admin.register(CelestialBodyBiome)
class CelestialBodyBiomeAdmin(ModelAdmin):
    list_display = ("name", "celestial_body")
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ("name", "star_system", "celestial_body", "location_type", "status")
    list_filter = ("location_type", "status", "star_system", "is_armistice_zone")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(JumpPoint)
class JumpPointAdmin(ModelAdmin):
    list_display = ("name", "source_system", "destination_system", "size", "status")
    list_filter = ("size", "status", "is_bidirectional")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(AsteroidBelt)
class AsteroidBeltAdmin(ModelAdmin):
    list_display = ("name", "star_system", "mineable", "status")
    list_filter = ("status", "mineable")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
