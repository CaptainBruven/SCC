import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from scc.utils.models import TimeStampedModel


class Tag(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    tag_group = models.CharField(max_length=50, blank=True, default="")

    class Meta(TimeStampedModel.Meta):
        db_table = "tag"

    def __str__(self):
        return f"{self.name}"


class Taggable(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="taggables")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        db_table = "taggable"
        unique_together = [("tag", "content_type", "object_id")]

    def __str__(self):
        return f"{self.tag} → {self.content_type}:{self.object_id}"


class Media(TimeStampedModel):
    class MediaType:
        IMAGE = 0
        VIDEO = 1
        PDF = 2

        CHOICES = [
            (IMAGE, "Image"),
            (VIDEO, "Video"),
            (PDF, "PDF"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=500)
    media_type = models.IntegerField(choices=MediaType.CHOICES)
    caption = models.CharField(max_length=300, blank=True)
    source = models.CharField(max_length=200, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    sort_order = models.IntegerField(default=0)

    class Meta(TimeStampedModel.Meta):
        db_table = "media"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.caption or self.url}"


class GameVersion(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True)
    release_date = models.DateField(null=True, blank=True)
    is_live = models.BooleanField()
    is_ptu = models.BooleanField()
    patch_notes_url = models.URLField(max_length=500, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "game_version"

    def __str__(self):
        return f"{self.version}"


class DataSource(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    base_url = models.URLField(max_length=500, blank=True)
    api_url = models.URLField(max_length=500, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "data_source"

    def __str__(self):
        return f"{self.name}"
