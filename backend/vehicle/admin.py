from django.contrib import admin

from vehicle.models import (
    Vehicle,
    VehicleHardpoint,
    VehicleImage,
    VehicleLoanerEntry,
    VehiclePaint,
    VehicleTag,
    VehicleTagAssignment,
    VehicleVariant,
)


class VehicleHardpointInline(admin.TabularInline):
    model = VehicleHardpoint
    extra = 0
    fields = ("hardpoint_name", "hardpoint_type", "size", "quantity", "mount_type", "default_component")


class VehicleVariantInline(admin.TabularInline):
    model = VehicleVariant
    fk_name = "base_vehicle"
    extra = 0


class VehiclePaintInline(admin.TabularInline):
    model = VehiclePaint
    extra = 0
    fields = ("name", "source", "price_usd", "price_auec")


class VehicleTagAssignmentInline(admin.TabularInline):
    model = VehicleTagAssignment
    extra = 0


class VehicleLoanerEntryInline(admin.TabularInline):
    model = VehicleLoanerEntry
    fk_name = "pledged_vehicle"
    extra = 0


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 0
    fields = ("image_url", "image_type", "caption", "is_primary", "sort_order")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "vehicle_type", "size_class", "status", "pledge_price_usd")
    list_filter = ("vehicle_type", "size_class", "status", "manufacturer", "pledge_availability", "is_alien")
    search_fields = ("name", "slug", "series")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        VehicleHardpointInline,
        VehicleVariantInline,
        VehiclePaintInline,
        VehicleTagAssignmentInline,
        VehicleLoanerEntryInline,
        VehicleImageInline,
    ]


@admin.register(VehicleHardpoint)
class VehicleHardpointAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "hardpoint_name", "hardpoint_type", "size", "quantity", "mount_type")
    list_filter = ("hardpoint_type", "mount_type")
    search_fields = ("hardpoint_name", "vehicle__name")


@admin.register(VehicleVariant)
class VehicleVariantAdmin(admin.ModelAdmin):
    list_display = ("base_vehicle", "variant_vehicle", "relationship_type")
    list_filter = ("relationship_type",)
    search_fields = ("base_vehicle__name", "variant_vehicle__name")


@admin.register(VehiclePaint)
class VehiclePaintAdmin(admin.ModelAdmin):
    list_display = ("name", "vehicle", "source", "price_usd", "price_auec")
    list_filter = ("source",)
    search_fields = ("name", "vehicle__name")


@admin.register(VehicleTag)
class VehicleTagAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(VehicleTagAssignment)
class VehicleTagAssignmentAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "tag")
    list_filter = ("tag",)


@admin.register(VehicleLoanerEntry)
class VehicleLoanerEntryAdmin(admin.ModelAdmin):
    list_display = ("pledged_vehicle", "loaner_vehicle", "loaner_context")
    list_filter = ("loaner_context",)
    search_fields = ("pledged_vehicle__name", "loaner_vehicle__name")


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "image_type", "caption", "is_primary", "sort_order")
    list_filter = ("image_type", "is_primary")
    search_fields = ("vehicle__name", "caption")
