from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    user = models.ForeignKey(
        "auth.User",
        blank=True,
        null=True,
        related_name="user_%(class)s_objects",
        on_delete=models.CASCADE,
    )
    who = models.ForeignKey(
        "auth.User",
        blank=True,
        null=True,
        related_name="who_%(class)s_objects",
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey("users.NotificationSubject", on_delete=models.CASCADE)

    amount = models.CharField(max_length=128, null=True, blank=True)

    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "users_notification"
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        ordering = ("-time",)

    class Admin:
        list_display = ("subject",)

    def __str__(self):
        return self.subject.name


class NotificationSubject(models.Model):
    code = models.CharField(max_length=128)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "users_notification_subject"
        verbose_name = _("notification subject")
        verbose_name_plural = _("notification subjects")
        ordering = ("name",)

    class Admin:
        list_display = ("name",)

    def __str__(self):
        return self.name


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
