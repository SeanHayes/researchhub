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
	
	def __unicode__(self):
		return unicode(self.user)

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
	description   = models.TextField(blank=True, help_text="Description/purpose of this study.")
	location      = models.TextField(blank=True, help_text="Location this study will take place, directions if needed.")
	contact_info  = models.TextField(blank=True, help_text="Phone/email/etc.")
	irb_number    = models.CharField(max_length=255)
	irb_proposal  = models.FileField(max_length=255, upload_to='irb_proposals/%Y/%m/%d/')
	survey        = models.TextField(blank=True, help_text="HTML to embed Survey")
	status        = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_DRAFT, help_text="Draft surveys will not yet be visible to users. Set to Published to make visible.")
	compensation  = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Amount participants will be paid.")
	created       = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	
	#TODO: move this stuff to a Group model (specify number of participants for a demographic)
	earliest_birthdate = models.DateField(null=True, blank=True, help_text="Earliest birthdate of eligible participants.")
	latest_birthdate   = models.DateField(null=True, blank=True, help_text="Latest birthdate of eligible participants.")
	gender             = models.IntegerField(choices=SubjectProfile.GENDER_CHOICES, null=True, blank=True, help_text="Restrict to a specific gender.")
	additional_criteria  = models.TextField(blank=True, help_text="Additional criteria participants need to meet that may not be specified elsewhere.")
	
	def __unicode__(self):
		return u'%s at %s (IRB #%s)' % (self.title, self.institution, self.irb_number,)
	
	class Meta:
		ordering = ('-created',)
		verbose_name_plural = 'studies'

