import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from scc.utils.models import TimeStampedModel
from universe.models import Location, StarSystem


class Species(TimeStampedModel):
    class Classification:
        SENTIENT = 0
        DEVELOPING = 1
        EXTINCT = 2

        CHOICES = [
            (SENTIENT, "Sentient"),
            (DEVELOPING, "Developing"),
            (EXTINCT, "Extinct"),
        ]

    class RelationToHumans:
        ALLIED = 0
        NEUTRAL = 1
        HOSTILE = 2
        UNKNOWN = 3
        ASSIMILATED = 4

        CHOICES = [
            (ALLIED, "Allied"),
            (NEUTRAL, "Neutral"),
            (HOSTILE, "Hostile"),
            (UNKNOWN, "Unknown"),
            (ASSIMILATED, "Assimilated"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    classification = models.IntegerField(choices=Classification.CHOICES)
    description = models.TextField(
        blank=True,
    )
    homeworld = models.CharField(
        max_length=100,
        blank=True,
    )
    government_type = models.CharField(
        max_length=100,
        blank=True,
    )
    language = models.CharField(
        max_length=100,
        blank=True,
    )
    lifespan = models.CharField(
        max_length=50,
        blank=True,
    )
    physical_description = models.TextField(
        blank=True,
    )
    cultural_notes = models.TextField(
        blank=True,
    )
    relation_to_humans = models.IntegerField(choices=RelationToHumans.CHOICES)
    wiki_url = models.URLField(
        max_length=500,
        blank=True,
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
    )

    class Meta(TimeStampedModel.Meta):
        db_table = "species"
        verbose_name_plural = "species"

    def __str__(self):
        return f"{self.name}"


class SpeciesRelation(TimeStampedModel):
    class RelationType:
        ALLIED = 0
        NEUTRAL = 1
        TENSE = 2
        HOSTILE = 3
        WAR = 4
        TRADE_ONLY = 5
        UNKNOWN = 6

        CHOICES = [
            (ALLIED, "Allied"),
            (NEUTRAL, "Neutral"),
            (TENSE, "Tense"),
            (HOSTILE, "Hostile"),
            (WAR, "War"),
            (TRADE_ONLY, "Trade Only"),
            (UNKNOWN, "Unknown"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    species_a = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="relations_as_a")
    species_b = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="relations_as_b")
    relation_type = models.IntegerField(choices=RelationType.CHOICES)
    description = models.TextField(
        blank=True,
    )

    class Meta(TimeStampedModel.Meta):
        db_table = "species_relation"
        unique_together = [("species_a", "species_b")]

    def __str__(self):
        return f"{self.species_a} ↔ {self.species_b}: {self.relation_type}"


class Faction(TimeStampedModel):
    class FactionType:
        GOVERNMENT = 0
        CORPORATION = 1
        MILITARY = 2
        PIRATE = 3
        CRIMINAL = 4
        RELIGIOUS = 5
        TRADE_GUILD = 6
        OTHER = 7

        CHOICES = [
            (GOVERNMENT, "Government"),
            (CORPORATION, "Corporation"),
            (MILITARY, "Military"),
            (PIRATE, "Pirate"),
            (CRIMINAL, "Criminal"),
            (RELIGIOUS, "Religious"),
            (TRADE_GUILD, "Trade Guild"),
            (OTHER, "Other"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True, blank=True, related_name="factions")
    faction_type = models.IntegerField(choices=FactionType.CHOICES)
    description = models.TextField(
        blank=True,
    )
    headquarters = models.CharField(
        max_length=200,
        blank=True,
    )
    is_lawful = models.BooleanField(null=True, blank=True)
    wiki_url = models.URLField(
        max_length=500,
        blank=True,
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
    )

    class Meta(TimeStampedModel.Meta):
        db_table = "faction"

    def __str__(self):
        return f"{self.name}"


class MissionType(TimeStampedModel):
    class Category:
        COMBAT = 0
        TRADE = 1
        MINING = 2
        EXPLORATION = 3
        DELIVERY = 4
        INVESTIGATION = 5
        RESCUE = 6
        MERCENARY = 7
        PIRACY = 8
        SALVAGE = 9

        CHOICES = [
            (COMBAT, "Combat"),
            (TRADE, "Trade"),
            (MINING, "Mining"),
            (EXPLORATION, "Exploration"),
            (DELIVERY, "Delivery"),
            (INVESTIGATION, "Investigation"),
            (RESCUE, "Rescue"),
            (MERCENARY, "Mercenary"),
            (PIRACY, "Piracy"),
            (SALVAGE, "Salvage"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.IntegerField(
        choices=Category.CHOICES,
    )
    description = models.TextField(
        blank=True,
    )
    icon_url = models.URLField(
        max_length=500,
        blank=True,
    )

    class Meta(TimeStampedModel.Meta):
        db_table = "mission_type"

    def __str__(self):
        return f"{self.name}"


class MissionGiver(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(
        blank=True,
    )
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="mission_givers")
    faction = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True, related_name="mission_givers")
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="mission_givers")
    image_url = models.URLField(
        max_length=500,
        blank=True,
    )

    class Meta(TimeStampedModel.Meta):
        db_table = "mission_giver"

    def __str__(self):
        return f"{self.name}"


class Mission(TimeStampedModel):
    class Difficulty:
        EASY = 0
        MEDIUM = 1
        HARD = 2
        VERY_HARD = 3

        CHOICES = [
            (EASY, "Easy"),
            (MEDIUM, "Medium"),
            (HARD, "Hard"),
            (VERY_HARD, "Very Hard"),
        ]

    class Status:
        IN_GAME = 0
        PLANNED = 1
        REMOVED = 2

        CHOICES = [
            (IN_GAME, "In Game"),
            (PLANNED, "Planned"),
            (REMOVED, "Removed"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mission_type = models.ForeignKey(MissionType, on_delete=models.CASCADE, related_name="missions")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(
        blank=True,
    )
    mission_giver = models.ForeignKey(MissionGiver, on_delete=models.SET_NULL, null=True, blank=True, related_name="missions")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="missions")
    star_system = models.ForeignKey(StarSystem, on_delete=models.SET_NULL, null=True, blank=True, related_name="missions")
    min_reputation_required = models.IntegerField(null=True, blank=True)
    reputation_faction = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True, related_name="reputation_missions")
    reward_auec_min = models.IntegerField(null=True, blank=True)
    reward_auec_max = models.IntegerField(null=True, blank=True)
    reward_reputation = models.IntegerField(null=True, blank=True)
    difficulty = models.IntegerField(choices=Difficulty.CHOICES)
    is_lawful = models.BooleanField(null=True, blank=True)
    is_group_recommended = models.BooleanField()
    is_chain_mission = models.BooleanField()
    chain_order = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(
        choices=Status.CHOICES,
    )

    class Meta(TimeStampedModel.Meta):
        db_table = "mission"

    def __str__(self):
        return f"{self.name}"


class LoreArticle(TimeStampedModel):
    class Category:
        HISTORY = 0
        TECHNOLOGY = 1
        CULTURE = 2
        POLITICS = 3
        SCIENCE = 4
        BIOGRAPHY = 5
        EVENT = 6
        LOCATION = 7
        SPECIES = 8

        CHOICES = [
            (HISTORY, "History"),
            (TECHNOLOGY, "Technology"),
            (CULTURE, "Culture"),
            (POLITICS, "Politics"),
            (SCIENCE, "Science"),
            (BIOGRAPHY, "Biography"),
            (EVENT, "Event"),
            (LOCATION, "Location"),
            (SPECIES, "Species"),
        ]

    class Source:
        GALACTAPEDIA = 0
        COMM_LINK = 1
        JUMP_POINT = 2
        WRITERS_GUIDE = 3
        SPECTRUM = 4

        CHOICES = [
            (GALACTAPEDIA, "Galactapedia"),
            (COMM_LINK, "Comm-Link"),
            (JUMP_POINT, "Jump Point"),
            (WRITERS_GUIDE, "Writer's Guide"),
            (SPECTRUM, "Spectrum"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField(
        blank=True,
    )
    category = models.IntegerField(
        choices=Category.CHOICES,
    )
    source = models.IntegerField(
        choices=Source.CHOICES,
    )
    source_url = models.URLField(
        max_length=500,
        blank=True,
    )
    publication_date = models.DateField(null=True, blank=True)
    lore_date = models.CharField(
        max_length=50,
        blank=True,
    )
    wiki_url = models.URLField(
        max_length=500,
        blank=True,
    )

    class Meta(TimeStampedModel.Meta):
        db_table = "lore_article"

    def __str__(self):
        return f"{self.title}"


class LoreArticleEntity(TimeStampedModel):
    class EntityType:
        STAR_SYSTEM = 0
        CELESTIAL_BODY = 1
        LOCATION = 2
        SPECIES = 3
        FACTION = 4
        VEHICLE = 5
        MANUFACTURER = 6
        PERSON = 7

        CHOICES = [
            (STAR_SYSTEM, "Star System"),
            (CELESTIAL_BODY, "Celestial Body"),
            (LOCATION, "Location"),
            (SPECIES, "Species"),
            (FACTION, "Faction"),
            (VEHICLE, "Vehicle"),
            (MANUFACTURER, "Manufacturer"),
            (PERSON, "Person"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lore_article = models.ForeignKey(LoreArticle, on_delete=models.CASCADE, related_name="entities")
    entity_type = models.IntegerField(choices=EntityType.CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    entity = GenericForeignKey("content_type", "object_id")

    class Meta(TimeStampedModel.Meta):
        db_table = "lore_article_entity"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.lore_article} → {self.entity_type}"
