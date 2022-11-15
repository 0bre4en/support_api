from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.username = username
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password=password)
        user.is_admin = True
        user.username = username
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    objects = UserManager()

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[username_validator],
    )
    email = models.EmailField(blank=False, unique=True)
    is_support = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
