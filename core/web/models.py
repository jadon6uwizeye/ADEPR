import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username, full_name, password=None, **extra_fields
    ):
        """
        Creates and saves a admin with the given email and password.
        """
        user = self.create_user(
            email,
            username,
            full_name,
            password=password,
            **extra_fields,
        )
        user.is_active = True
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    def search_user(self, name):
        return self.filter(
            Q(username__icontains=name) | Q(full_name__icontains=name)
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    This is the base user model that is used for authentication
    """
    USER = 1
    ADMIN = 2
    USER_TYPE_CHOICE = (
        (USER, "User"),
        (ADMIN, "Administartor"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField("email address", max_length=255, unique=True)
    full_name = models.CharField(_("full name"), max_length=100)
    username = models.CharField(_("username"), max_length=100, unique=True)

    # unique phone number as it is a medium for user recognition
    phone_number = models.CharField(
        _("phone number"), max_length=255, blank=True, null=True, unique=True
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(_("about"), null=True, blank=True)
    user_type = models.IntegerField(
        _("user type"), choices=USER_TYPE_CHOICE, default=USER
    )
    is_active = models.BooleanField(_("is active"), default=False)
    # a admin user; non super-user
    staff = models.BooleanField(_("staff"), default=False)
    admin = models.BooleanField(_("admin"), default=False) 
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = _("username")
    REQUIRED_FIELDS = ["email", "full_name"]

    class Meta:
        ordering = ['full_name']


    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.full_name

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

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


class Member(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itorero = models.ForeignKey(Itorero, verbose_name=_("Itorero arimo"), on_delete=models.CASCADE)


    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Member_detail", kwargs={"pk": self.pk})
