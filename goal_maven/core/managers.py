"""
Managers for Database models.
"""
from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model
from django.db import models


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        self.validate_fields(email, **extra_fields)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a new superuser."""
        self.validate_fields(email, **extra_fields)

        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def update_user(self, user, **extra_fields):
        """Update and return an existing user."""
        self.validate_fields(user.email, **extra_fields)
        if 'email' in extra_fields:
            user.email = extra_fields['email']
            # raise ValueError(_('Email cannot be updated.'))
        if 'password' in extra_fields:
            user.set_password(extra_fields['password'])
        if 'first_name' in extra_fields:
            user.first_name = extra_fields['first_name']
        if 'last_name' in extra_fields:
            user.last_name = extra_fields['last_name']
        if 'date_of_birth' in extra_fields:
            date_of_birth = extra_fields['date_of_birth']
            try:
                self.validate_date_of_birth(date_of_birth)
            except ValidationError as e:
                raise ValidationError(e)
            user.date_of_birth = date_of_birth
        if 'country' in extra_fields:
            user.country = extra_fields['country']
        if 'favorite_team' in extra_fields:
            user.favorite_team = extra_fields['favorite_team']
        if 'favorite_players' in extra_fields:
            user.favorite_players = extra_fields['favorite_players']
        user.save(using=self._db)

        return user

    def validate_fields(self, email, **params):
        """Validates the provided fields."""

        if not email:
            raise ValueError(_('User must have an email address.'))
        if 'first_name' not in params:
            raise ValueError(_('User must have a First Name.'))
        if 'last_name' not in params:
            raise ValueError(_('User must have a Last Name.'))
        if 'date_of_birth' in params:
            try:
                self.validate_date_of_birth(params['date_of_birth'])
            except ValidationError as e:
                raise ValidationError(e)

    def validate_date_of_birth(self, date_of_birth):
        """Validate date_of_birth is not in the future or less than 5 years old."""
        date_of_birth_str = datetime.strptime(str(date_of_birth), '%Y-%m-%d')
        if date_of_birth_str > datetime.now():
            raise ValidationError(_(
                'Date of birth cannot be in the future.'
            ))
        if date_of_birth_str > datetime.now() - timedelta(days=1825):
            raise ValidationError(_(
                'You have be 5 years or older to use this api.'
            ))


class SuperuserOnlyManager(models.Manager):
    """Common manager to ensure only staff can create an object."""
    # if not user.is_superuser:
    #     raise ValueError("Permission Denied")
    def create(self, user=None, *args, **kwargs):
        if not user:
            return super().create(*args, **kwargs)
        if user.is_staff:
            return super().create(*args, **kwargs)
        raise ValueError("Permission Denied")
