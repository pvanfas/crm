from django.db import models
from django.utils.translation import gettext_lazy as _


class Permission(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    app = models.CharField(max_length=128)

    class Meta:
        db_table = "permission"
        verbose_name = _("permission")
        verbose_name_plural = _("permissions")
        ordering = ("app",)

    class Admin:
        list_display = ("id", "name", "code", "app")

    def __str__(self):
        return self.name + " - " + self.app
