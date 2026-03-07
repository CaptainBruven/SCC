import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from scc.utils.models import TimeStampedModel
from universe.models import Location


class CommodityCategory(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    class Meta(TimeStampedModel.Meta):
        db_table = "commodity_category"
        verbose_name_plural = "commodity categories"

    def __str__(self):
        return f"{self.name}"


class Commodity(TimeStampedModel):
    class Legality:
        LEGAL = 0
        ILLEGAL = 1
        RESTRICTED = 2
        CONTRABAND = 3

        CHOICES = [
            (LEGAL, "Legal"),
            (ILLEGAL, "Illegal"),
            (RESTRICTED, "Restricted"),
            (CONTRABAND, "Contraband"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commodity_category = models.ForeignKey(CommodityCategory, on_delete=models.CASCADE, related_name="commodities")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    legality = models.IntegerField(choices=Legality.CHOICES)
    base_price_auec = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_mineable = models.BooleanField()
    is_tradeable = models.BooleanField(default=True)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "commodity"
        verbose_name_plural = "commodities"

    def __str__(self):
        return f"{self.name}"


class CommodityPriceEntry(TimeStampedModel):
    class TransactionType:
        BUY = 0
        SELL = 1

        CHOICES = [
            (BUY, "Buy"),
            (SELL, "Sell"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, related_name="price_entries")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="commodity_prices")
    transaction_type = models.IntegerField(choices=TransactionType.CHOICES)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    recorded_at = models.DateTimeField()
    supply_demand_status = models.CharField(max_length=50, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "commodity_price_entry"
        verbose_name_plural = "commodity price entries"
        indexes = [
            models.Index(fields=["commodity", "location", "transaction_type"]),
            models.Index(fields=["recorded_at"]),
        ]

    def __str__(self):
        return f"{self.commodity} @ {self.location}: {self.price_per_unit}"


class MiningResource(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, related_name="mining_resources")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    instability = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    resistance = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    optimal_charge_window = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "mining_resource"

    def __str__(self):
        return f"{self.name}"


class Shop(TimeStampedModel):
    class ShopType:
        WEAPONS = 0
        ARMOR = 1
        COMPONENTS = 2
        CLOTHING = 3
        COMMODITY = 4
        FOOD = 5
        GENERAL = 6
        SHIP_DEALER = 7
        VEHICLE_RENTAL = 8
        REFINERY = 9

        CHOICES = [
            (WEAPONS, "Weapons"),
            (ARMOR, "Armor"),
            (COMPONENTS, "Components"),
            (CLOTHING, "Clothing"),
            (COMMODITY, "Commodity"),
            (FOOD, "Food"),
            (GENERAL, "General"),
            (SHIP_DEALER, "Ship Dealer"),
            (VEHICLE_RENTAL, "Vehicle Rental"),
            (REFINERY, "Refinery"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="shops")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    shop_type = models.IntegerField(choices=ShopType.CHOICES)
    description = models.TextField(blank=True)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "shop"

    def __str__(self):
        return f"{self.name}"


class ShopInventory(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="inventory")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    item = GenericForeignKey("content_type", "object_id")
    price_auec = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "shop_inventory"
        verbose_name_plural = "shop inventories"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.shop} — {self.content_type}:{self.object_id}"
