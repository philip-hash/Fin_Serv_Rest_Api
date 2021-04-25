from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager



class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)
        #hash_password= make_password(password)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email

class LargeCap(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    tick = models.TextField(blank=True,primary_key=True)
    close = models.FloatField(blank=True, null=True)
    price_action_probability = models.FloatField(blank=True, null=True)
    reversal_probability = models.FloatField(blank=True, null=True)
    volitility_probability = models.FloatField(blank=True, null=True)
    sentiment_strength = models.FloatField(blank=True, null=True)
    liquidity_rating = models.FloatField(db_column='Liquidity_rating', blank=True, null=True)  # Field name made lowercase.
    debt_rating = models.FloatField(db_column='Debt_rating', blank=True, null=True)  # Field name made lowercase.
    productivity_rating = models.FloatField(db_column='Productivity_rating', blank=True, null=True)  # Field name made lowercase.
    growth_rating = models.FloatField(db_column='Growth_rating', blank=True, null=True)  # Field name made lowercase.
    market_rating = models.FloatField(db_column='Market_rating', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Large_Cap'