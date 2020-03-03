from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from sorl import thumbnail
# from .helpers import get_upload_path
from django.contrib.auth.models import User
from .utils.constants import GENDER_CHOICES, MARTIAL_CHOICES 
from django.contrib.auth import get_user_model

USER = get_user_model()

class Location(models.Model):
      
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255,  blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)



class CustomUser(models.Model):

    user = models.OneToOneField(USER, on_delete=models.CASCADE,  related_name='profile')
  
    profile_picture = thumbnail.ImageField(
        upload_to='documents/',
        blank=True
    )

    email = models.EmailField(
        _('email address'), null=True,
        unique=True,
    )
  
    gender = models.CharField(
        max_length=10,  
        choices=GENDER_CHOICES,
        blank=True, null=True
    )
   
    martial_status = models.CharField(
        max_length=10,  
        choices=MARTIAL_CHOICES,
        blank=True, null=True
    )
    dob = models.DateField(
        _("Date of Birth"), blank=True, null=True)

    current_address = models.ForeignKey(
        Location, null=True, blank=True,
        related_name='current_address_users',
        on_delete=models.SET_NULL)

    permanent_address = models.ForeignKey(
        Location, null=True, blank=True,
        related_name='permanent_address_users',
        on_delete=models.SET_NULL
    )
 
    
 

  
 