from django.contrib import admin

from core.models import DataSource, GameVersion, Media, Tag, Taggable


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "tag_group", "slug")
    list_filter = ("tag_group",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Taggable)
class TaggableAdmin(admin.ModelAdmin):
    list_display = ("tag", "content_type", "object_id")
    list_filter = ("content_type",)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("caption", "media_type", "content_type", "sort_order")
    list_filter = ("media_type", "content_type")
    search_fields = ("caption", "url")


@admin.register(GameVersion)
class GameVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "name", "release_date", "is_live", "is_ptu")
    list_filter = ("is_live", "is_ptu")
    search_fields = ("version", "name")


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "base_url", "last_synced_at")
    search_fields = ("name",)
