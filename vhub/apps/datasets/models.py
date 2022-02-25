from django.db import models
from django.utils.translation import gettext_lazy as _


class Datasets(models.Model):
    """Class that represents the Vulnerabilities Dataset."""

    name = models.CharField(
        max_length=100, blank=False, default="Unnamed"
    )
    file = models.FileField(
        _("file"), upload_to="datasets", blank=False, null=False
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    owner = models.ForeignKey(
        to="user.User",
        related_name="datasets",
        on_delete=models.CASCADE,
        verbose_name=_("owner")
    )

    class Meta:
        ordering = ["created_at", "name"]
        db_table = "datasets"
        verbose_name = "datasets"
        verbose_name_plural = "datasets"
