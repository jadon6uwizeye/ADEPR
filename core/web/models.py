import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models import Q
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
    NID = models.CharField(_("National ID"), max_length=50)
    father_names = models.CharField(_("fathers' name"), max_length=50, null=True) 
    mother_names = models.CharField(_("mothers' name"), max_length=50, null=True)
    date_of_birth = models.CharField(_("date of birth"),max_length=50, null=True, blank=True)
    place_of_birth = models.CharField(_("place of birth"), max_length=50, null=True)
    birth_country = models.CharField(_("birth country"), max_length=50, null=True)
    village = models.CharField(_("Village"), max_length=50, null=True)
    cell = models.CharField(_("Cell"), max_length=50, null=True)
    sector = models.CharField(_("Sector"), max_length=50, null=True)
    district = models.CharField(_("District"), max_length=50, null=True)
    province = models.CharField(_("Province"), max_length=50, null=True)
    marital_status = models.CharField(_("marital status"), max_length=50, null=True)
    spouse = models.CharField(_("spouse"), max_length=50, null=True, blank=True)
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


