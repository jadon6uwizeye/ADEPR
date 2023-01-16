from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django.utils.translation import gettext as _

from web.models import User

# User = get_user_model()

# Create your models here.

class Region(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Region_detail", kwargs={"pk": self.pk})


class Ururembo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _("Ururembo")
        verbose_name_plural = _("Indembo")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Ururembo_detail", kwargs={"pk": self.pk})


class Parish(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    ururembo = models.ForeignKey(Ururembo, on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    

    class Meta:
        verbose_name = _("Parish")
        verbose_name_plural = _("Parishes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("parish_detail", kwargs={"pk": self.pk})



class LocalChurch(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _("Local church")
        verbose_name_plural = _("Amatorero")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("local _church_detail", kwargs={"pk": self.pk})

