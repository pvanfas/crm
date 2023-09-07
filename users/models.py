from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    app = models.CharField(max_length=128)

    class Meta:
        ordering = ("app",)

    def __str__(self):
        return f'{self.name} - {self.app}'
