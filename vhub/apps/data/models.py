from django.utils.translation import gettext_lazy as _
from django.db import models


class Data(models.Model):
    """Class that represents the Vulnerabilities Data."""

    SEVERITY_CHOICES = (
        ("low", _("Low")),
        ("medium", _("Medium")),
        ("high", _("High")),
        ("critical", _("Critical")),
    )

    hostname = models.CharField(max_length=100, blank=False, default="Unnamed")
    ip_address = models.CharField(
        _("IP address"),
        max_length=100,
        blank=False,
        null=True,
        editable=False
    )
    title = models.TextField(_("title"), blank=False, default="Untitled")
    severity = models.CharField(
        _("severity"),
        max_length=50,
        choices=SEVERITY_CHOICES,
        blank=False,
        null=True,
        editable=False
    )
    cvss = models.FloatField(blank=False, null=True)
    publication_date = models.DateTimeField(
        _("publication date"),
        blank=False,
        null=True,
    )
    solved = models.BooleanField(_("solved"), blank=False, default=False)
    dataset = models.ForeignKey(
        to="datasets.Datasets", related_name="data", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["hostname", "ip_address", "title", "severity"]
        db_table = "data"
        verbose_name = "data"
        verbose_name_plural = "data"
