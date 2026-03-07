import uuid

from django.db import models

from component.models import Component
from manufacturer.models import Manufacturer
from scc.utils.models import TimeStampedModel


class Vehicle(TimeStampedModel):
    class VehicleType:
        SPACESHIP = 0
        GROUND_VEHICLE = 1
        GRAVLEV = 2

        CHOICES = [
            (SPACESHIP, "Spaceship"),
            (GROUND_VEHICLE, "Ground Vehicle"),
            (GRAVLEV, "Gravlev"),
        ]

    class SizeClass:
        SNUB = 0
        SMALL = 1
        MEDIUM = 2
        LARGE = 3
        CAPITAL = 4

        CHOICES = [
            (SNUB, "Snub"),
            (SMALL, "Small"),
            (MEDIUM, "Medium"),
            (LARGE, "Large"),
            (CAPITAL, "Capital"),
        ]

    class Status:
        FLIGHT_READY = 0
        IN_CONCEPT = 1
        IN_PRODUCTION = 2
        ANNOUNCED = 3
        LORE_ONLY = 4

        CHOICES = [
            (FLIGHT_READY, "Flight Ready"),
            (IN_CONCEPT, "In Concept"),
            (IN_PRODUCTION, "In Production"),
            (ANNOUNCED, "Announced"),
            (LORE_ONLY, "Lore Only"),
        ]

    class PledgeAvailability:
        PERMANENT = 0
        LIMITED = 1
        CONCIERGE = 2
        EVENT = 3
        NOT_AVAILABLE = 4

        CHOICES = [
            (PERMANENT, "Permanent"),
            (LIMITED, "Limited"),
            (CONCIERGE, "Concierge"),
            (EVENT, "Event"),
            (NOT_AVAILABLE, "Not Available"),
        ]

    class PadSize:
        XS = 0
        SMALL = 1
        MEDIUM = 2
        LARGE = 3
        XL = 4
        HANGAR = 5

        CHOICES = [
            (XS, "XS"),
            (SMALL, "Small"),
            (MEDIUM, "Medium"),
            (LARGE, "Large"),
            (XL, "XL"),
            (HANGAR, "Hangar"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="vehicles")
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    series = models.CharField(max_length=100, blank=True)
    vehicle_type = models.IntegerField(choices=VehicleType.CHOICES)
    size_class = models.IntegerField(choices=SizeClass.CHOICES)
    focus_primary = models.CharField(max_length=100, blank=True)
    focus_secondary = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    lore_description = models.TextField(blank=True)
    status = models.IntegerField(choices=Status.CHOICES)
    is_alien = models.BooleanField()
    min_crew = models.IntegerField(null=True, blank=True)
    max_crew = models.IntegerField(null=True, blank=True)
    cargo_capacity_scu = models.IntegerField(null=True, blank=True)
    length_m = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    beam_m = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    height_m = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    mass_kg = models.IntegerField(null=True, blank=True)
    combat_speed_ms = models.IntegerField(null=True, blank=True)
    max_speed_ms = models.IntegerField(null=True, blank=True)
    scm_speed_ms = models.IntegerField(null=True, blank=True)
    hydrogen_fuel_capacity = models.IntegerField(null=True, blank=True)
    quantum_fuel_capacity = models.IntegerField(null=True, blank=True)
    pledge_price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ingame_price_auec = models.IntegerField(null=True, blank=True)
    warbond_price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pledge_availability = models.IntegerField(choices=PledgeAvailability.CHOICES)
    insurance_claim_time_s = models.IntegerField(null=True, blank=True)
    expedited_claim_time_s = models.IntegerField(null=True, blank=True)
    expedited_claim_cost = models.IntegerField(null=True, blank=True)
    has_quantum_drive = models.BooleanField(default=True)
    has_bed = models.BooleanField()
    has_interior = models.BooleanField()
    can_carry_vehicle = models.BooleanField()
    pad_size = models.IntegerField(choices=PadSize.CHOICES)
    added_in_patch = models.CharField(max_length=20, blank=True)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    brochure_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "vehicle"
        indexes = [
            models.Index(fields=["manufacturer", "status"]),
            models.Index(fields=["size_class"]),
        ]

    def __str__(self):
        return f"{self.name}"


class VehicleHardpoint(TimeStampedModel):
    class HardpointType:
        WEAPON = 0
        MISSILE_RACK = 1
        TURRET = 2
        POWER_PLANT = 3
        COOLER = 4
        SHIELD_GENERATOR = 5
        QUANTUM_DRIVE = 6
        RADAR = 7
        COMPUTER = 8
        LIFE_SUPPORT = 9
        MINING_LASER = 10
        SALVAGE_HEAD = 11
        TRACTOR_BEAM = 12
        FUEL_POD = 13
        CARGO_GRID = 14
        VEHICLE_MODULE = 15
        UTILITY = 16

        CHOICES = [
            (WEAPON, "Weapon"),
            (MISSILE_RACK, "Missile Rack"),
            (TURRET, "Turret"),
            (POWER_PLANT, "Power Plant"),
            (COOLER, "Cooler"),
            (SHIELD_GENERATOR, "Shield Generator"),
            (QUANTUM_DRIVE, "Quantum Drive"),
            (RADAR, "Radar"),
            (COMPUTER, "Computer"),
            (LIFE_SUPPORT, "Life Support"),
            (MINING_LASER, "Mining Laser"),
            (SALVAGE_HEAD, "Salvage Head"),
            (TRACTOR_BEAM, "Tractor Beam"),
            (FUEL_POD, "Fuel Pod"),
            (CARGO_GRID, "Cargo Grid"),
            (VEHICLE_MODULE, "Vehicle Module"),
            (UTILITY, "Utility"),
        ]

    class MountType:
        FIXED = 0
        GIMBAL = 1
        TURRET = 2
        REMOTE_TURRET = 3
        UNMANNED_TURRET = 4

        CHOICES = [
            (FIXED, "Fixed"),
            (GIMBAL, "Gimbal"),
            (TURRET, "Turret"),
            (REMOTE_TURRET, "Remote Turret"),
            (UNMANNED_TURRET, "Unmanned Turret"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="hardpoints")
    hardpoint_name = models.CharField(max_length=100)
    hardpoint_type = models.IntegerField(choices=HardpointType.CHOICES)
    size = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    is_gimbal = models.BooleanField()
    is_turret = models.BooleanField()
    is_manned = models.BooleanField()
    is_remote = models.BooleanField()
    default_component = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name="default_on_hardpoints")
    mount_type = models.IntegerField(choices=MountType.CHOICES)

    class Meta(TimeStampedModel.Meta):
        db_table = "vehicle_hardpoint"

    def __str__(self):
        return f"{self.vehicle} — {self.hardpoint_name}"


class VehicleVariant(TimeStampedModel):
    class RelationshipType:
        VARIANT = 0
        UPGRADE = 1
        EDITION = 2
        MILITARY_CIVILIAN = 3

        CHOICES = [
            (VARIANT, "Variant"),
            (UPGRADE, "Upgrade"),
            (EDITION, "Edition"),
            (MILITARY_CIVILIAN, "Military/Civilian"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    base_vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="variants_as_base")
    variant_vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="variants_as_variant")
    relationship_type = models.IntegerField(choices=RelationshipType.CHOICES)

    class Meta(TimeStampedModel.Meta):
        db_table = "vehicle_variant"
        unique_together = [("base_vehicle", "variant_vehicle")]

    def __str__(self):
        return f"{self.base_vehicle} → {self.variant_vehicle}"


class VehiclePaint(TimeStampedModel):
    class Source:
        PLEDGE = 0
        INGAME_PURCHASE = 1
        EVENT = 2
        SUBSCRIBER = 3
        REFERRAL = 4

        CHOICES = [
            (PLEDGE, "Pledge"),
            (INGAME_PURCHASE, "In-Game Purchase"),
            (EVENT, "Event"),
            (SUBSCRIBER, "Subscriber"),
            (REFERRAL, "Referral"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="paints")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    source = models.IntegerField(choices=Source.CHOICES)
    price_usd = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_auec = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "vehicle_paint"

    def __str__(self):
        return f"{self.vehicle} — {self.name}"


class VehicleTag(TimeStampedModel):
    class Category:
        ROLE = 0
        GAMEPLAY = 1
        SPECIAL = 2

        CHOICES = [
            (ROLE, "Role"),
            (GAMEPLAY, "Gameplay"),
            (SPECIAL, "Special"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    category = models.IntegerField(choices=Category.CHOICES)
    description = models.TextField(blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "vehicle_tag"

    def __str__(self):
        return f"{self.name}"


class VehicleTagAssignment(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="tag_assignments")
    tag = models.ForeignKey(VehicleTag, on_delete=models.CASCADE, related_name="vehicle_assignments")

    class Meta:
        db_table = "vehicle_tag_assignment"
        unique_together = [("vehicle", "tag")]

    def __str__(self):
        return f"{self.vehicle} — {self.tag}"


class VehicleLoanerEntry(TimeStampedModel):
    class LoanerContext:
        PU = 0
        AC = 1

        CHOICES = [
            (PU, "Persistent Universe"),
            (AC, "Arena Commander"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pledged_vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="loaner_entries_as_pledged")
    loaner_vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="loaner_entries_as_loaner")
    loaner_context = models.IntegerField(choices=LoanerContext.CHOICES)

    class Meta(TimeStampedModel.Meta):
        db_table = "vehicle_loaner_entry"

    def __str__(self):
        return f"{self.pledged_vehicle} → {self.loaner_vehicle}"


class VehicleImage(TimeStampedModel):
    class ImageType:
        EXTERIOR = 0
        INTERIOR = 1
        COCKPIT = 2
        CARGO = 3
        BROCHURE = 4
        CONCEPT_ART = 5
        SCREENSHOT = 6

        CHOICES = [
            (EXTERIOR, "Exterior"),
            (INTERIOR, "Interior"),
            (COCKPIT, "Cockpit"),
            (CARGO, "Cargo"),
            (BROCHURE, "Brochure"),
            (CONCEPT_ART, "Concept Art"),
            (SCREENSHOT, "Screenshot"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=500)
    caption = models.CharField(max_length=200, blank=True)
    image_type = models.IntegerField(choices=ImageType.CHOICES)
    is_primary = models.BooleanField()
    sort_order = models.IntegerField(default=0)

    class Meta(TimeStampedModel.Meta):
        db_table = "vehicle_image"

    def __str__(self):
        return f"{self.vehicle} — {self.image_type or 'image'}"
