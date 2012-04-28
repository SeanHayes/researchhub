#Python imports
import logging

#Django imports
from django.contrib.auth.models import User
from django.db import models

#App imports
from managers import StudyManager

logger = logging.getLogger(__name__)

# Create your models here.

class Institution(models.Model):
	name = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		ordering = ('name',)


class SubjectProfile(models.Model):
	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_CHOICES = (
		(GENDER_MALE, 'Male',),
		(GENDER_FEMALE, 'Female',),
	)
	user          = models.OneToOneField(User)
	birthdate     = models.DateField()
	gender        = models.IntegerField(choices=GENDER_CHOICES)
	city          = models.CharField(max_length=255)
	state         = models.CharField(max_length=255)
	postal_code   = models.CharField(max_length=10)
	country       = models.CharField(max_length=255)
	last_modified = models.DateTimeField(auto_now=True)

class Study(models.Model):
	STATUS_DRAFT = 0
	STATUS_PUBLISHED = 1
	STATUS_CHOICES = (
		(STATUS_DRAFT, 'Draft',),
		(STATUS_PUBLISHED, 'Published',),
	)
	
	objects = StudyManager()
	
	user          = models.ForeignKey(User, help_text="The user posting this study.")
	title         = models.CharField(max_length=255)
	institution   = models.ForeignKey(Institution)
	description   = models.TextField(blank=True)
	location      = models.TextField(blank=True)
	irb_number    = models.CharField(max_length=255)
	irb_proposal  = models.FileField(max_length=255, upload_to='irb_proposals/%Y/%m/%d/')
	survey        = models.TextField(blank=True)
	status        = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_DRAFT)
	created       = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	
	#TODO: move this stuff to a Group model (specify number of participants for a demographic)
	earliest_birthdate = models.DateField(null=True, blank=True)
	latest_birthdate   = models.DateField(null=True, blank=True)
	gender             = models.IntegerField(choices=SubjectProfile.GENDER_CHOICES, null=True, blank=True)
	
	def __unicode__(self):
		return u'%s at %s (#%s)' % (self.title, self.institution, self.irb_number,)
	
	class Meta:
		ordering = ('-created',)

