from django.contrib import admin

from equipment.models import (
    ArmorPiece,
    Clothing,
    PersonalArmor,
    PersonalWeapon,
    Tool,
    Undersuit,
    WeaponAttachment,
    WeaponAttachmentCompatibility,
)


class WeaponAttachmentCompatibilityInline(admin.TabularInline):
    model = WeaponAttachmentCompatibility
    extra = 0


@admin.register(PersonalWeapon)
class PersonalWeaponAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "weapon_class", "damage_type", "rarity", "status", "price_auec")
    list_filter = ("weapon_class", "damage_type", "rarity", "status", "manufacturer")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [WeaponAttachmentCompatibilityInline]


@admin.register(WeaponAttachment)
class WeaponAttachmentAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "attachment_type", "price_auec")
    list_filter = ("attachment_type", "manufacturer")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(WeaponAttachmentCompatibility)
class WeaponAttachmentCompatibilityAdmin(admin.ModelAdmin):
    list_display = ("weapon", "attachment", "slot_type")
    list_filter = ("slot_type",)
    search_fields = ("weapon__name", "attachment__name")


class ArmorPieceInline(admin.TabularInline):
    model = ArmorPiece
    extra = 0
    fields = ("name", "slot", "armor_type", "price_auec")


@admin.register(PersonalArmor)
class PersonalArmorAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "armor_type", "armor_category", "rarity", "price_auec")
    list_filter = ("armor_type", "armor_category", "rarity", "manufacturer")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ArmorPieceInline]


@admin.register(ArmorPiece)
class ArmorPieceAdmin(admin.ModelAdmin):
    list_display = ("name", "armor_set", "manufacturer", "slot", "armor_type", "price_auec")
    list_filter = ("slot", "armor_type", "manufacturer")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Undersuit)
class UndersuitAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "has_eva_capability", "inventory_slots", "price_auec")
    list_filter = ("has_eva_capability", "manufacturer")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Clothing)
class ClothingAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "clothing_type", "price_auec")
    list_filter = ("clothing_type", "manufacturer")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "tool_type", "price_auec")
    list_filter = ("tool_type", "manufacturer")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
