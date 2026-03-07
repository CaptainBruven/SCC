from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from component.models import (
    Component,
    ComponentCategory,
    ComponentSpecCooler,
    ComponentSpecMissile,
    ComponentSpecPowerPlant,
    ComponentSpecQuantumDrive,
    ComponentSpecShield,
    ComponentSpecWeapon,
)


@admin.register(ComponentCategory)
class ComponentCategoryAdmin(ModelAdmin):
    list_display = ("name", "slug", "parent_category")
    list_filter = ("parent_category",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ComponentSpecQuantumDriveInline(StackedInline):
    model = ComponentSpecQuantumDrive
    extra = 0


class ComponentSpecShieldInline(StackedInline):
    model = ComponentSpecShield
    extra = 0


class ComponentSpecPowerPlantInline(StackedInline):
    model = ComponentSpecPowerPlant
    extra = 0


class ComponentSpecCoolerInline(StackedInline):
    model = ComponentSpecCooler
    extra = 0


class ComponentSpecWeaponInline(StackedInline):
    model = ComponentSpecWeapon
    extra = 0


class ComponentSpecMissileInline(StackedInline):
    model = ComponentSpecMissile
    extra = 0


@admin.register(Component)
class ComponentAdmin(ModelAdmin):
    list_display = ("name", "component_category", "manufacturer", "size", "grade", "class_type", "status")
    list_filter = ("component_category", "grade", "class_type", "status", "manufacturer")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ComponentSpecQuantumDriveInline,
        ComponentSpecShieldInline,
        ComponentSpecPowerPlantInline,
        ComponentSpecCoolerInline,
        ComponentSpecWeaponInline,
        ComponentSpecMissileInline,
    ]


@admin.register(ComponentSpecQuantumDrive)
class ComponentSpecQuantumDriveAdmin(ModelAdmin):
    list_display = ("component", "quantum_speed_mps", "spool_time_s", "fuel_consumption_lmkm")
    search_fields = ("component__name",)


@admin.register(ComponentSpecShield)
class ComponentSpecShieldAdmin(ModelAdmin):
    list_display = ("component", "shield_hp", "regen_rate", "regen_delay_s")
    search_fields = ("component__name",)


@admin.register(ComponentSpecPowerPlant)
class ComponentSpecPowerPlantAdmin(ModelAdmin):
    list_display = ("component", "power_output")
    search_fields = ("component__name",)


@admin.register(ComponentSpecCooler)
class ComponentSpecCoolerAdmin(ModelAdmin):
    list_display = ("component", "cooling_rate")
    search_fields = ("component__name",)


@admin.register(ComponentSpecWeapon)
class ComponentSpecWeaponAdmin(ModelAdmin):
    list_display = ("component", "weapon_type", "damage_type", "dps", "fire_rate_rpm")
    list_filter = ("weapon_type", "damage_type")
    search_fields = ("component__name",)


@admin.register(ComponentSpecMissile)
class ComponentSpecMissileAdmin(ModelAdmin):
    list_display = ("component", "missile_type", "tracking_type", "damage", "speed_ms")
    list_filter = ("missile_type", "tracking_type")
    search_fields = ("component__name",)
