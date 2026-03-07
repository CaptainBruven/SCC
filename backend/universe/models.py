import uuid

from django.db import models

from scc.utils.models import TimeStampedModel


class StarSystem(TimeStampedModel):
    class Status:
        IN_GAME = 0
        PLANNED = 1
        LORE_ONLY = 2

        CHOICES = [
            (IN_GAME, "In Game"),
            (PLANNED, "Planned"),
            (LORE_ONLY, "Lore Only"),
        ]

    class Affiliation:
        UEE = 0
        UNCLAIMED = 1
        VANDUUL = 2
        XIAN = 3
        BANU = 4
        DEVELOPING = 5
        DISPUTED = 6

        CHOICES = [
            (UEE, "UEE"),
            (UNCLAIMED, "Unclaimed"),
            (VANDUUL, "Vanduul"),
            (XIAN, "Xi'an"),
            (BANU, "Banu"),
            (DEVELOPING, "Developing"),
            (DISPUTED, "Disputed"),
        ]

    class ThreatLevel:
        LOW = 0
        MEDIUM = 1
        HIGH = 2
        HOSTILE = 3

        CHOICES = [
            (LOW, "Low"),
            (MEDIUM, "Medium"),
            (HIGH, "High"),
            (HOSTILE, "Hostile"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=Status.CHOICES)
    affiliation = models.IntegerField(choices=Affiliation.CHOICES)
    population = models.CharField(max_length=50, blank=True)
    economy = models.CharField(max_length=50, blank=True)
    threat_level = models.IntegerField(choices=ThreatLevel.CHOICES)
    star_type = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=20, blank=True)
    discovery_date_lore = models.CharField(max_length=20, blank=True)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "star_system"

    def __str__(self):
        return f"{self.name}"


class Star(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    star_system = models.ForeignKey(StarSystem, on_delete=models.CASCADE, related_name="stars")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    star_type = models.CharField(max_length=50, blank=True)
    spectral_class = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    habitable_zone_inner_au = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    habitable_zone_outer_au = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "star"

    def __str__(self):
        return f"{self.name}"


class CelestialBody(TimeStampedModel):
    class BodyType:
        PLANET = 0
        MOON = 1
        PLANETOID = 2
        ASTEROID = 3

        CHOICES = [
            (PLANET, "Planet"),
            (MOON, "Moon"),
            (PLANETOID, "Planetoid"),
            (ASTEROID, "Asteroid"),
        ]

    class ThreatLevel:
        LOW = 0
        MEDIUM = 1
        HIGH = 2

        CHOICES = [
            (LOW, "Low"),
            (MEDIUM, "Medium"),
            (HIGH, "High"),
        ]

    class Status:
        IN_GAME = 0
        PLANNED = 1
        LORE_ONLY = 2

        CHOICES = [
            (IN_GAME, "In Game"),
            (PLANNED, "Planned"),
            (LORE_ONLY, "Lore Only"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    star_system = models.ForeignKey(StarSystem, on_delete=models.CASCADE, related_name="celestial_bodies")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    body_type = models.IntegerField(choices=BodyType.CHOICES)
    classification = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    atmosphere = models.CharField(max_length=50, blank=True)
    atmosphere_details = models.TextField(blank=True)
    habitable = models.BooleanField()
    has_natural_satellites = models.BooleanField()
    orbital_period = models.CharField(max_length=50, blank=True)
    distance_from_star_au = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    size_km = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    gravity = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    temperature_range = models.CharField(max_length=100, blank=True)
    owner_entity = models.CharField(max_length=100, blank=True)
    threat_level = models.IntegerField(choices=ThreatLevel.CHOICES)
    status = models.IntegerField(choices=Status.CHOICES)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    added_in_patch = models.CharField(max_length=20, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "celestial_body"
        verbose_name_plural = "celestial bodies"
        indexes = [
            models.Index(fields=["star_system", "body_type"]),
            models.Index(fields=["parent"]),
        ]

    def __str__(self):
        return f"{self.name}"


class CelestialBodyBiome(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    celestial_body = models.ForeignKey(CelestialBody, on_delete=models.CASCADE, related_name="biomes")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "celestial_body_biome"

    def __str__(self):
        return f"{self.name}"


class Location(TimeStampedModel):
    class LocationType:
        LANDING_ZONE = 0
        SPACE_STATION = 1
        OUTPOST = 2
        SETTLEMENT = 3
        REST_STOP = 4
        REFINERY = 5
        CAVE = 6
        WRECK = 7
        COMM_ARRAY = 8
        SECURITY_POST = 9
        JUMP_POINT_GATEWAY = 10
        OTHER = 11

        CHOICES = [
            (LANDING_ZONE, "Landing Zone"),
            (SPACE_STATION, "Space Station"),
            (OUTPOST, "Outpost"),
            (SETTLEMENT, "Settlement"),
            (REST_STOP, "Rest Stop"),
            (REFINERY, "Refinery"),
            (CAVE, "Cave"),
            (WRECK, "Wreck"),
            (COMM_ARRAY, "Comm Array"),
            (SECURITY_POST, "Security Post"),
            (JUMP_POINT_GATEWAY, "Jump Point Gateway"),
            (OTHER, "Other"),
        ]

    class Status:
        IN_GAME = 0
        PLANNED = 1
        LORE_ONLY = 2

        CHOICES = [
            (IN_GAME, "In Game"),
            (PLANNED, "Planned"),
            (LORE_ONLY, "Lore Only"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    star_system = models.ForeignKey(StarSystem, on_delete=models.CASCADE, related_name="locations")
    celestial_body = models.ForeignKey(CelestialBody, on_delete=models.CASCADE, null=True, blank=True, related_name="locations")
    parent_location = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    location_type = models.IntegerField(choices=LocationType.CHOICES)
    sub_type = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_armistice_zone = models.BooleanField()
    has_refuel = models.BooleanField()
    has_repair = models.BooleanField()
    has_medical = models.BooleanField()
    has_cargo_terminal = models.BooleanField()
    has_refinery = models.BooleanField()
    has_vehicle_spawn = models.BooleanField()
    has_ground_vehicle_spawn = models.BooleanField()
    has_habitation = models.BooleanField()
    jurisdiction = models.CharField(max_length=100, blank=True)
    crime_stat_allowed = models.BooleanField()
    coordinates_x = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    coordinates_y = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    coordinates_z = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    status = models.IntegerField(choices=Status.CHOICES)
    wiki_url = models.URLField(max_length=500, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    added_in_patch = models.CharField(max_length=20, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "location"
        indexes = [
            models.Index(fields=["star_system", "location_type"]),
            models.Index(fields=["celestial_body"]),
        ]

    def __str__(self):
        return f"{self.name}"


class JumpPoint(TimeStampedModel):
    class Size:
        SMALL = 0
        MEDIUM = 1
        LARGE = 2

        CHOICES = [
            (SMALL, "Small"),
            (MEDIUM, "Medium"),
            (LARGE, "Large"),
        ]

    class Status:
        IN_GAME = 0
        PLANNED = 1
        LORE_ONLY = 2

        CHOICES = [
            (IN_GAME, "In Game"),
            (PLANNED, "Planned"),
            (LORE_ONLY, "Lore Only"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    source_system = models.ForeignKey(StarSystem, on_delete=models.CASCADE, related_name="jump_points_out")
    destination_system = models.ForeignKey(StarSystem, on_delete=models.CASCADE, related_name="jump_points_in")
    size = models.IntegerField(choices=Size.CHOICES)
    status = models.IntegerField(choices=Status.CHOICES)
    description = models.TextField(blank=True)
    is_bidirectional = models.BooleanField(default=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "jump_point"

    def __str__(self):
        return f"{self.name}" or f"{self.source_system} → {self.destination_system}"


class AsteroidBelt(TimeStampedModel):
    class Status:
        IN_GAME = 0
        PLANNED = 1
        LORE_ONLY = 2

        CHOICES = [
            (IN_GAME, "In Game"),
            (PLANNED, "Planned"),
            (LORE_ONLY, "Lore Only"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    star_system = models.ForeignKey(StarSystem, on_delete=models.CASCADE, related_name="asteroid_belts")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    mineable = models.BooleanField()
    resources = models.TextField(blank=True)
    distance_au = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    status = models.IntegerField(choices=Status.CHOICES)

    class Meta(TimeStampedModel.Meta):
        db_table = "asteroid_belt"

    def __str__(self):
        return f"{self.name}"
