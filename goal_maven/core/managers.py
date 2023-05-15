"""
Managers for Database models.
"""
from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


import inspect


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, **extra_fields):
        """Create, save and return a new user."""
        self.validate_fields(email, **extra_fields)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(extra_fields['password'])
        user.save(using=self._db)

        return user

    def create_superuser(self, email, **extra_fields):
        """Create and return a new superuser."""

        user = self.create_user(email, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def update_user(self, user, **extra_fields):
        """Update and return an existing user."""
        self.validate_fields(user.email, **extra_fields)
        if 'password' in extra_fields:
            user.set_password(extra_fields['password'])
        if 'first_name' in extra_fields:
            user.first_name = extra_fields['first_name']
        if 'last_name' in extra_fields:
            user.last_name = extra_fields['last_name']
        if 'date_of_birth' in extra_fields:
            user.date_of_birth = extra_fields['date_of_birth']
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
        from goal_maven.core.models import (
            Nation,
            Team,
            Player,
        )
        for k, v in params.items():
            if v == '':
                raise ValueError(_(f"'{k}' cannot be empty."))

        caller_method = inspect.currentframe().f_back.f_code.co_name
        user_exists = get_user_model().objects.filter(
            email=email,
        ).exists()
        if not user_exists:
            if 'update' in caller_method:
                raise ValueError(_('User with provided email address does not exist.'))
        else:
            if 'create' in caller_method:
                raise ValueError(_('User with provided email already exists.'))

        if 'create' in caller_method:
            if 'password' not in params:
                raise ValueError(_('User must have a password.'))
            if 'first_name' not in params:
                raise ValueError(_('User must have a First Name.'))
            if 'last_name' not in params:
                raise ValueError(_('User must have a Last Name.'))
            if 'username' not in params:
                raise ValueError(_('User must have a username.'))

        if 'date_of_birth' in params:
            try:
                self.validate_date_of_birth(params['date_of_birth'])
            except ValidationError as e:
                raise ValidationError(e)
        else:
            raise ValueError(_('User must have a date of birth.'))

        if 'country' in params:
            nation_exists = Nation.objects.filter(
                nation_name=params['country'],
            ).exists()
            if not nation_exists:
                raise ValueError(_('Country provided does not exist.'))

        if 'favorite_team' in params:
            for team in params['favorite_team']:
                team_exists = Team.objects.filter(
                    team_name=team,
                ).exists()
                if not team_exists:
                    raise ValueError(_(f"Team '{team}' does not exist."))

        if 'favorite_players' in params:
            for player in params['favorite_players']:
                player_exists = Player.objects.filter(
                    player_name=player,
                ).exists()
                if not player_exists:
                    raise ValueError(_(f"Player '{player}' does not exist."))

    def validate_date_of_birth(self, date_of_birth):
        """Validate date_of_birth is not in the future or less than 5 years old."""
        if date_of_birth > datetime.now().date():
            raise ValidationError(_(
                'Date of birth cannot be in the future.'
            ))
        if date_of_birth > datetime.now().date() - timedelta(days=1825):
            raise ValidationError(_(
                'You have be 5 years or older to use this api.'
            ))
