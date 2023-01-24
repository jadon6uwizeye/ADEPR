import uuid
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from amatorero.models import LocalChurch

User = get_user_model()

# Create your models here.


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)
class Member(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='church_members')
    gender = models.CharField(_("gender"), max_length=50, choices=GENDER_CHOICES)
    # local_church = models.ForeignKey(LocalChurch, verbose_name=_("Local church"), on_delete=models.CASCADE)


    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return self.user.full_name

    def get_absolute_url(self):
        return reverse("Member_detail", kwargs={"pk": self.pk})


class OfferingCategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = _("Offering category")
        verbose_name_plural = _("Offering categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Offering_category_detail", kwargs={"pk": self.pk})


class Offering(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    details = models.TextField()
    category = models.ForeignKey(OfferingCategory, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    recorder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    local_church = models.ForeignKey(LocalChurch, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Offering")
        verbose_name_plural = _("Offerings")

    def __str__(self):
        # return date created_on without time formatted to string
        return str(self.created_on.strftime("%d-%m-%Y"))

    def get_absolute_url(self):
        return reverse("Offering_detail", kwargs={"pk": self.pk})


class Document(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(_("name of the document"), max_length=50)    
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Document_detail", kwargs={"pk": self.pk})

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
)

class DocumentRequest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    details = models.TextField(_("some details for the document being requested"))
    status = models.CharField(_("choices"), max_length=50, choices=STATUS_CHOICES)
    local_church = models.ForeignKey(LocalChurch, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = _("Document request")
        verbose_name_plural = _("Document requests")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Document_request_detail", kwargs={"pk": self.pk})
