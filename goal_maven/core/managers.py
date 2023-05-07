"""
Managers for Database models.
"""
from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        date_of_birth = extra_fields.get('date_of_birth')
        if date_of_birth:
            try:
                self.validate_date_of_birth(date_of_birth)
            except ValidationError as e:
                raise ValidationError(_('Invalid date of birth')) from e
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a new superuser."""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def validate_date_of_birth(self, date_of_birth):
        """Validate date_of_birth is not in the future or less than 5 years old."""
        date_of_birth_str = datetime.strptime(date_of_birth, '%Y-%m-%d')
        if date_of_birth_str > datetime.now():
            raise ValidationError(_('Date of birth cannot be in the future.'))
        if date_of_birth_str > datetime.now() - timedelta(days=1825):
            raise ValidationError(_(
                'You have be 5 years or older to use this api.'
            ))
