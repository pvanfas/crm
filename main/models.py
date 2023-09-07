import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey(
        "auth.User", blank=True, related_name="creator_%(class)s_objects", on_delete=models.CASCADE
    )
    updater = models.ForeignKey(
        "auth.User", blank=True, related_name="updator_%(class)s_objects", on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Mode(models.Model):
    readonly = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    down = models.BooleanField(default=False)

    class Meta:
        db_table = "mode"
        verbose_name = "mode"
        verbose_name_plural = "mode"
        ordering = ("id",)

    class Admin:
        list_display = ("id", "readonly", "maintenance", "down")

    def __str__(self):
        return str(self.id)
