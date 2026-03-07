import uuid

from django.db import models

from manufacturer.models import Manufacturer
from scc.utils.models import TimeStampedModel


class ComponentCategory(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    class Meta(TimeStampedModel.Meta):
        db_table = "component_category"
        verbose_name_plural = "component categories"

    def __str__(self):
        return f"{self.name}"


class Component(TimeStampedModel):
    class Grade:
        A = 0
        B = 1
        C = 2
        D = 3

    class ClassType:
        MILITARY = 0
        CIVILIAN = 1
        STEALTH = 2
        INDUSTRIAL = 3
        COMPETITION = 4

    class Status:
        IN_GAME = 0
        PLANNED = 1
        REMOVED = 2

    GRADE_CHOICES = [
        (Grade.A, "A"),
        (Grade.B, "B"),
        (Grade.C, "C"),
        (Grade.D, "D"),
    ]

    CLASS_TYPE_CHOICES = [
        (ClassType.MILITARY, "Military"),
        (ClassType.CIVILIAN, "Civilian"),
        (ClassType.STEALTH, "Stealth"),
        (ClassType.INDUSTRIAL, "Industrial"),
        (ClassType.COMPETITION, "Competition"),
    ]

    STATUS_CHOICES = [
        (Status.IN_GAME, "In Game"),
        (Status.PLANNED, "Planned"),
        (Status.REMOVED, "Removed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component_category = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE, related_name="components")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="components")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    size = models.IntegerField(null=True, blank=True)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    class_type = models.IntegerField(choices=CLASS_TYPE_CHOICES)
    durability_hp = models.IntegerField(null=True, blank=True)
    power_draw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    thermal_output = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    em_signature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ir_signature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mass_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_loot_only = models.BooleanField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    price_auec = models.IntegerField(null=True, blank=True)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "component"
        indexes = [
            models.Index(fields=["component_category", "size", "grade"]),
        ]

    def __str__(self):
        return self.name


class ComponentSpecQuantumDrive(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="spec_quantum_drive")
    quantum_speed_mps = models.IntegerField(null=True, blank=True)
    quantum_speed_c = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    spool_time_s = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fuel_consumption_lmkm = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    cooldown_time_s = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    calibration_speed = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    drive_stage = models.IntegerField(null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "component_spec_quantum_drive"

    def __str__(self):
        return f"QD Spec: {self.component}"


class ComponentSpecShield(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="spec_shield")
    shield_hp = models.IntegerField(null=True, blank=True)
    regen_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    regen_delay_s = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    ballistic_resistance = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    energy_resistance = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    distortion_resistance = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "component_spec_shield"

    def __str__(self):
        return f"Shield Spec: {self.component}"


class ComponentSpecPowerPlant(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="spec_power_plant")
    power_output = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "component_spec_power_plant"

    def __str__(self):
        return f"Power Plant Spec: {self.component}"


class ComponentSpecCooler(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="spec_cooler")
    cooling_rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "component_spec_cooler"

    def __str__(self):
        return f"Cooler Spec: {self.component}"


class ComponentSpecWeapon(TimeStampedModel):
    class WeaponType:
        CANNON = 0
        REPEATER = 1
        GATLING = 2
        SCATTERGUN = 3
        DISTORTION = 4
        LASER = 5

        CHOICES = [
            (CANNON, "Cannon"),
            (REPEATER, "Repeater"),
            (GATLING, "Gatling"),
            (SCATTERGUN, "Scattergun"),
            (DISTORTION, "Distortion"),
            (LASER, "Laser"),
        ]

    class DamageType:
        ENERGY = 0
        BALLISTIC = 1
        DISTORTION = 2
        MIXED = 3

        CHOICES = [
            (ENERGY, "Energy"),
            (BALLISTIC, "Ballistic"),
            (DISTORTION, "Distortion"),
            (MIXED, "Mixed"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="spec_weapon")
    weapon_type = models.IntegerField(choices=WeaponType.CHOICES)
    damage_type = models.IntegerField(choices=DamageType.CHOICES)
    fire_rate_rpm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    damage_per_shot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    projectile_speed_ms = models.IntegerField(null=True, blank=True)
    range_m = models.IntegerField(null=True, blank=True)
    ammo_capacity = models.IntegerField(null=True, blank=True)
    pellets_per_shot = models.IntegerField(null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "component_spec_weapon"

    def __str__(self):
        return f"Weapon Spec: {self.component}"


class ComponentSpecMissile(TimeStampedModel):
    class MissileType:
        MISSILE = 0
        TORPEDO = 1
        BOMB = 2
        ROCKET = 3

        CHOICES = [
            (MISSILE, "Missile"),
            (TORPEDO, "Torpedo"),
            (BOMB, "Bomb"),
            (ROCKET, "Rocket"),
        ]

    class TrackingType:
        IR = 0
        EM = 1
        CS = 2
        NONE = 3

        CHOICES = [
            (IR, "Infrared"),
            (EM, "Electromagnetic"),
            (CS, "Cross-Section"),
            (NONE, "None"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="spec_missile")
    missile_type = models.IntegerField(choices=MissileType.CHOICES)
    tracking_type = models.IntegerField(choices=TrackingType.CHOICES)
    damage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lock_time_s = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    speed_ms = models.IntegerField(null=True, blank=True)
    range_m = models.IntegerField(null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "component_spec_missile"

    def __str__(self):
        return f"Missile Spec: {self.component}"
