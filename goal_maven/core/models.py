"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from goal_maven.core.managers import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(_('Email ID'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=50, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=50, blank=True)
    username = models.CharField(_('Username'), max_length=50, blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    country = models.CharField(_('Country'), max_length=255, blank=True)
    favorite_team = models.CharField(_('Favorite Team'), max_length=255, blank=True)
    favorite_players = models.TextField(_('Favorite Players'), blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
