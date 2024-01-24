import uuid

from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name=_("country name"))
    iso_code_2d = models.CharField(max_length=2, verbose_name=_("iso code 2d"), unique=True, null=True, blank=True)
    iso_code_3d = models.CharField(max_length=3, verbose_name=_("iso code 3d"), unique=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        db_table = "Country"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['iso_code_2d']),
            models.Index(fields=['iso_code_3d']),
        ]

    def __str__(self):
        return self.name


class IP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=20, verbose_name=_("ip address"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="ips", verbose_name=_("country"), null=True, blank=True)

    class Meta:
        verbose_name = _("IP")
        verbose_name_plural = _("IPs")
        db_table = "IP"
        indexes = [
            models.Index(fields=['address']),
            models.Index(fields=['country']),
        ]

    def __str__(self):
        return f"{self.address} | {self.country.name}"

    def save(self, *args, **kwargs):
        try:
            validate_ipv46_address(self.address)
        except ValidationError:
            return
        super(IP, self).save(*args, **kwargs)
