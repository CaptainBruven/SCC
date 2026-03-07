import uuid

from django.db import models

from lore.models import Species
from scc.utils.models import TimeStampedModel


class Manufacturer(TimeStampedModel):
    class ManufacturerType:
        SHIP = 0
        COMPONENT = 1
        WEAPON = 2
        PERSONAL_WEAPON = 3
        ARMOR = 4
        CLOTHING = 5
        MULTI = 6

        CHOICES = [
            (SHIP, "Ship"),
            (COMPONENT, "Component"),
            (WEAPON, "Weapon"),
            (PERSONAL_WEAPON, "Personal Weapon"),
            (ARMOR, "Armor"),
            (CLOTHING, "Clothing"),
            (MULTI, "Multi"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(
        blank=True,
    )
    manufacturer_type = models.IntegerField(choices=ManufacturerType.CHOICES)
    origin = models.CharField(
        max_length=100,
        blank=True,
    )
    headquarters = models.CharField(
        max_length=200,
        blank=True,
    )
    founding_date_lore = models.CharField(
        max_length=50,
        blank=True,
    )
    is_alien = models.BooleanField()
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True, blank=True, related_name="manufacturers")
    logo_url = models.URLField(
        max_length=500,
        blank=True,
    )
    wiki_url = models.URLField(
        max_length=500,
        blank=True,
    )

    class Meta(TimeStampedModel.Meta):
        db_table = "manufacturer"

    def __str__(self):
        return f"{self.name}"
