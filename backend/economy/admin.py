from django.contrib import admin

from economy.models import (
    Commodity,
    CommodityCategory,
    CommodityPriceEntry,
    MiningResource,
    Shop,
    ShopInventory,
)


@admin.register(CommodityCategory)
class CommodityCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent_category")
    list_filter = ("parent_category",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ("name", "commodity_category", "legality", "base_price_auec", "is_mineable", "is_tradeable")
    list_filter = ("commodity_category", "legality", "is_mineable", "is_tradeable")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CommodityPriceEntry)
class CommodityPriceEntryAdmin(admin.ModelAdmin):
    list_display = ("commodity", "location", "transaction_type", "price_per_unit", "recorded_at")
    list_filter = ("transaction_type", "commodity", "location")
    search_fields = ("commodity__name", "location__name")


@admin.register(MiningResource)
class MiningResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "commodity", "instability", "resistance")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ShopInventoryInline(admin.TabularInline):
    model = ShopInventory
    extra = 0
    fields = ("content_type", "object_id", "price_auec", "is_available")


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "shop_type")
    list_filter = ("shop_type", "location")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ShopInventoryInline]


@admin.register(ShopInventory)
class ShopInventoryAdmin(admin.ModelAdmin):
    list_display = ("shop", "content_type", "object_id", "price_auec", "is_available")
    list_filter = ("is_available", "content_type", "shop")
