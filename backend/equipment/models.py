import uuid

from django.db import models

from manufacturer.models import Manufacturer
from scc.utils.models import TimeStampedModel


class PersonalWeapon(TimeStampedModel):
    class WeaponClass:
        PISTOL = 0
        SMG = 1
        ASSAULT_RIFLE = 2
        SHOTGUN = 3
        SNIPER_RIFLE = 4
        LMG = 5
        LAUNCHER = 6
        RAILGUN = 7
        CROSSBOW = 8
        KNIFE = 9
        MELEE = 10

        CHOICES = [
            (PISTOL, "Pistol"),
            (SMG, "SMG"),
            (ASSAULT_RIFLE, "Assault Rifle"),
            (SHOTGUN, "Shotgun"),
            (SNIPER_RIFLE, "Sniper Rifle"),
            (LMG, "LMG"),
            (LAUNCHER, "Launcher"),
            (RAILGUN, "Railgun"),
            (CROSSBOW, "Crossbow"),
            (KNIFE, "Knife"),
            (MELEE, "Melee"),
        ]

    class DamageType:
        BALLISTIC = 0
        ENERGY = 1
        PLASMA = 2
        DISTORTION = 3
        MIXED = 4

        CHOICES = [
            (BALLISTIC, "Ballistic"),
            (ENERGY, "Energy"),
            (PLASMA, "Plasma"),
            (DISTORTION, "Distortion"),
            (MIXED, "Mixed"),
        ]

    class Rarity:
        COMMON = 0
        UNCOMMON = 1
        RARE = 2
        VERY_RARE = 3
        LOOT_ONLY = 4

        CHOICES = [
            (COMMON, "Common"),
            (UNCOMMON, "Uncommon"),
            (RARE, "Rare"),
            (VERY_RARE, "Very Rare"),
            (LOOT_ONLY, "Loot Only"),
        ]

    class Status:
        IN_GAME = 0
        PLANNED = 1

        CHOICES = [
            (IN_GAME, "In Game"),
            (PLANNED, "Planned"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="personal_weapons")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    weapon_class = models.IntegerField(choices=WeaponClass.CHOICES)
    damage_type = models.IntegerField(choices=DamageType.CHOICES)
    fire_modes = models.CharField(max_length=100, blank=True)
    fire_rate_rpm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    damage_per_shot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    effective_range_m = models.IntegerField(null=True, blank=True)
    max_range_m = models.IntegerField(null=True, blank=True)
    magazine_size = models.IntegerField(null=True, blank=True)
    ammo_type = models.CharField(max_length=50, blank=True)
    has_optic_slot = models.BooleanField()
    has_barrel_slot = models.BooleanField()
    has_underbarrel_slot = models.BooleanField()
    mass_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_auec = models.IntegerField(null=True, blank=True)
    rarity = models.IntegerField(choices=Rarity.CHOICES)
    status = models.IntegerField(choices=Status.CHOICES)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "personal_weapon"

    def __str__(self):
        return f"{self.name}"


class WeaponAttachment(TimeStampedModel):
    class AttachmentType:
        OPTIC = 0
        BARREL = 1
        UNDERBARREL = 2
        MAGAZINE = 3

        CHOICES = [
            (OPTIC, "Optic"),
            (BARREL, "Barrel"),
            (UNDERBARREL, "Underbarrel"),
            (MAGAZINE, "Magazine"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, related_name="weapon_attachments")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    attachment_type = models.IntegerField(choices=AttachmentType.CHOICES)
    description = models.TextField(blank=True)
    magnification = models.CharField(max_length=20, blank=True)
    price_auec = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "weapon_attachment"

    def __str__(self):
        return f"{self.name}"


class WeaponAttachmentCompatibility(models.Model):
    class SlotType:
        OPTIC = 0
        BARREL = 1
        UNDERBARREL = 2

        CHOICES = [
            (OPTIC, "Optic"),
            (BARREL, "Barrel"),
            (UNDERBARREL, "Underbarrel"),
        ]

    weapon = models.ForeignKey(PersonalWeapon, on_delete=models.CASCADE, related_name="attachment_compatibilities")
    attachment = models.ForeignKey(WeaponAttachment, on_delete=models.CASCADE, related_name="weapon_compatibilities")
    slot_type = models.IntegerField(choices=SlotType.CHOICES)

    class Meta:
        db_table = "weapon_attachment_compatibility"
        unique_together = [("weapon", "attachment")]

    def __str__(self):
        return f"{self.weapon} ↔ {self.attachment}"


class PersonalArmor(TimeStampedModel):
    class ArmorType:
        LIGHT = 0
        MEDIUM = 1
        HEAVY = 2

        CHOICES = [
            (LIGHT, "Light"),
            (MEDIUM, "Medium"),
            (HEAVY, "Heavy"),
        ]

    class ArmorCategory:
        COMBAT = 0
        SPECIALIST = 1
        UTILITY = 2
        SUPPORT = 3

        CHOICES = [
            (COMBAT, "Combat"),
            (SPECIALIST, "Specialist"),
            (UTILITY, "Utility"),
            (SUPPORT, "Support"),
        ]

    class Rarity:
        COMMON = 0
        UNCOMMON = 1
        RARE = 2
        VERY_RARE = 3

        CHOICES = [
            (COMMON, "Common"),
            (UNCOMMON, "Uncommon"),
            (RARE, "Rare"),
            (VERY_RARE, "Very Rare"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, related_name="personal_armors")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    armor_type = models.IntegerField(choices=ArmorType.CHOICES)
    armor_category = models.IntegerField(choices=ArmorCategory.CHOICES)
    damage_reduction_ballistic = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    damage_reduction_energy = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    temperature_resistance = models.CharField(max_length=50, blank=True)
    inventory_slots = models.IntegerField(null=True, blank=True)
    price_auec = models.IntegerField(null=True, blank=True)
    rarity = models.IntegerField(choices=Rarity.CHOICES)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "personal_armor"

    def __str__(self):
        return f"{self.name}"


class ArmorPiece(TimeStampedModel):
    class Slot:
        HELMET = 0
        CHEST = 1
        ARMS = 2
        LEGS = 3
        BACKPACK = 4

        CHOICES = [
            (HELMET, "Helmet"),
            (CHEST, "Chest"),
            (ARMS, "Arms"),
            (LEGS, "Legs"),
            (BACKPACK, "Backpack"),
        ]

    class ArmorType:
        LIGHT = 0
        MEDIUM = 1
        HEAVY = 2

        CHOICES = [
            (LIGHT, "Light"),
            (MEDIUM, "Medium"),
            (HEAVY, "Heavy"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    armor_set = models.ForeignKey(PersonalArmor, on_delete=models.SET_NULL, null=True, blank=True, related_name="pieces")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, related_name="armor_pieces")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    slot = models.IntegerField(choices=Slot.CHOICES)
    armor_type = models.IntegerField(choices=ArmorType.CHOICES)
    description = models.TextField(blank=True)
    price_auec = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "armor_piece"

    def __str__(self):
        return f"{self.name}"


class Undersuit(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, related_name="undersuits")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    temperature_range = models.CharField(max_length=100, blank=True)
    has_eva_capability = models.BooleanField()
    inventory_slots = models.IntegerField(null=True, blank=True)
    price_auec = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "undersuit"

    def __str__(self):
        return f"{self.name}"


class Clothing(TimeStampedModel):
    class ClothingType:
        JACKET = 0
        SHIRT = 1
        PANTS = 2
        SHOES = 3
        GLOVES = 4
        HAT = 5
        GLASSES = 6
        BACKPACK = 7
        ACCESSORY = 8

        CHOICES = [
            (JACKET, "Jacket"),
            (SHIRT, "Shirt"),
            (PANTS, "Pants"),
            (SHOES, "Shoes"),
            (GLOVES, "Gloves"),
            (HAT, "Hat"),
            (GLASSES, "Glasses"),
            (BACKPACK, "Backpack"),
            (ACCESSORY, "Accessory"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, related_name="clothing_items")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    clothing_type = models.IntegerField(choices=ClothingType.CHOICES)
    description = models.TextField(blank=True)
    price_auec = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "clothing"

    def __str__(self):
        return f"{self.name}"


class Tool(TimeStampedModel):
    class ToolType:
        MULTI_TOOL = 0
        MED_PEN = 1
        OXYPEN = 2
        FLARE = 3
        TRACTOR_BEAM_ATTACHMENT = 4
        MINING_ATTACHMENT = 5
        REPAIR_ATTACHMENT = 6
        SALVAGE_ATTACHMENT = 7

        CHOICES = [
            (MULTI_TOOL, "Multi-Tool"),
            (MED_PEN, "Med Pen"),
            (OXYPEN, "OxyPen"),
            (FLARE, "Flare"),
            (TRACTOR_BEAM_ATTACHMENT, "Tractor Beam Attachment"),
            (MINING_ATTACHMENT, "Mining Attachment"),
            (REPAIR_ATTACHMENT, "Repair Attachment"),
            (SALVAGE_ATTACHMENT, "Salvage Attachment"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, related_name="tools")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    tool_type = models.IntegerField(choices=ToolType.CHOICES)
    description = models.TextField(blank=True)
    price_auec = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "tool"

    def __str__(self):
        return f"{self.name}"
