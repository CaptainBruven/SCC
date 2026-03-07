from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from lore.models import (
    Faction,
    LoreArticle,
    LoreArticleEntity,
    Mission,
    MissionGiver,
    MissionType,
    Species,
    SpeciesRelation,
)


@admin.register(Species)
class SpeciesAdmin(ModelAdmin):
    list_display = ("name", "classification", "relation_to_humans", "homeworld")
    list_filter = ("classification", "relation_to_humans")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SpeciesRelation)
class SpeciesRelationAdmin(ModelAdmin):
    list_display = ("species_a", "species_b", "relation_type")
    list_filter = ("relation_type",)


@admin.register(Faction)
class FactionAdmin(ModelAdmin):
    list_display = ("name", "faction_type", "species", "is_lawful")
    list_filter = ("faction_type", "is_lawful", "species")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MissionType)
class MissionTypeAdmin(ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MissionGiver)
class MissionGiverAdmin(ModelAdmin):
    list_display = ("name", "faction", "species", "location")
    list_filter = ("faction", "species")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Mission)
class MissionAdmin(ModelAdmin):
    list_display = ("name", "mission_type", "difficulty", "status", "reward_auec_min", "reward_auec_max")
    list_filter = ("mission_type", "difficulty", "status", "is_lawful", "is_group_recommended")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class LoreArticleEntityInline(TabularInline):
    model = LoreArticleEntity
    extra = 0


@admin.register(LoreArticle)
class LoreArticleAdmin(ModelAdmin):
    list_display = ("title", "category", "source", "publication_date")
    list_filter = ("category", "source")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LoreArticleEntityInline]


@admin.register(LoreArticleEntity)
class LoreArticleEntityAdmin(ModelAdmin):
    list_display = ("lore_article", "entity_type", "content_type", "object_id")
    list_filter = ("entity_type", "content_type")
