#Python imports
import logging

#Django imports
from django.contrib.auth.models import User
from django.db import models

#App imports
from managers import *

logger = logging.getLogger(__name__)

# Create your models here.

class ResearchStudy(models.Model):
	title = models.TextField()
	#fields for institution, location (optional), IRB #, link to survey (optional), upload IRB proposal

GENDER_MALE = 0
GENDER_FEMALE = 1
GENDER_CHOICES = (
	(GENDER_MALE, 'Male',),
	(GENDER_FEMALE, 'Female',),
)

class SubjectProfile(User):
	birthdate = models.DateField()
	gender    = models.IntegerField(choices=GENDER_CHOICES)
	city      = models.CharField(max_length=255)
	state     = models.CharField(max_length=255)
	postal_code = models.CharField(max_length=10)
	country   = models.CharField(max_length=255)
	
