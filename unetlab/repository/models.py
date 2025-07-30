"""Define ORM models for Proxmox hosts."""

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse


class Repository(models.Model):
    """
    Model for Repository.

    The details of Repository are retrieved and cached.
    """

    name = models.CharField(primary_key=True, max_length=255)
    uri = models.CharField(max_length=255)
    is_enabled = models.BooleanField(
        default=True,
        help_text="False if Repository is disabled and should not be used.",
        verbose_name="Enabled",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        """Database metadata."""

        db_table = "repositories"
        ordering = ["name"]
        verbose_name = _("Repository")
        verbose_name_plural = _("Repositories")

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("repository-detail-view", args=[str(self.pk)])
