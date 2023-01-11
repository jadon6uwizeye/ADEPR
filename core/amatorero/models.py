from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django.utils.translation import gettext as _

from web.models import User

# User = get_user_model()

# Create your models here.

class Province(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Province_detail", kwargs={"pk": self.pk})


class District(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("District_detail", kwargs={"pk": self.pk})


class Sector(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Sector_detail", kwargs={"pk": self.pk})


class Cell(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    

    class Meta:
        verbose_name = _("Cell")
        verbose_name_plural = _("Cells")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Cell_detail", kwargs={"pk": self.pk})


class Itorero(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _("Itorero")
        verbose_name_plural = _("Amatorero")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Itorero_detail", kwargs={"pk": self.pk})

