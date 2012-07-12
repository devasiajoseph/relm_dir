from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from app.utilities import send_activation_email, create_key
from django.conf import settings
from django.core.context_processors import csrf
import re
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
import simplejson


class Country(models.Model):
    name = models.CharField(max_length=1024)


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    verification_key = models.CharField(max_length=1024)
    key_expires = models.DateTimeField(null=True)

    # directory based fields
    name = models.CharField(max_length=1024)
    address_line1 = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    country = models.ForeignKey(Country, null=True, blank=True)
    phone = models.CharField(max_length=20)
    user_type = models.CharField(max_length=10)


def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal for creating a new profile and setting activation key
    """

    if created:
        profile = UserProfile.objects.create(user=instance)

        if settings.EMAIL_VERIFICATION_REQUIRED:
            key_object = create_key(instance.username, 2)
            profile.verification_key = key_object["key"]
            profile.key_expires = key_object["expiry"]
            send_activation_email(instance.email, key_object["key"])

        profile.save()
    return

# connect to the signal
# post_save.connect(create_user_profile, sender=User)


class SellerRequest(models.Model):
    name = models.CharField(max_length=1024)
    address_line1 = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    country = models.ForeignKey(Country)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    approval_key = models.CharField(max_length=1024)
    key_expires = models.DateTimeField(null=True)
