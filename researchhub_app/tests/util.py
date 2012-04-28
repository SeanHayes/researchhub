#Python imports
from datetime import datetime

#Django imports
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

#App imports
from ..models import Institution, Study, SubjectProfile

class BaseTestCase(TestCase):
	def setUp(self):
		self.username = 'test_user'
		self.password = 'foobar'
		self.user1 = User.objects.create_user(self.username, 'test_user@example.com', self.password)
		self.user2 = User.objects.create_user('test_user2', 'test_user@example.com', self.password)
		
		profile1 = SubjectProfile(
			user=self.user1,
			gender=SubjectProfile.GENDER_MALE,
			birthdate=datetime(year=1986, month=9, day=9),
			city='Rochester',
			state='NY',
			postal_code='14611',
			country='US',
		)
		profile1.save()
		
		self.inst1 = Institution(name='University of Rochester')
		self.inst1.save()
		self.inst2 = Institution(name='Center for Disease Control')
		self.inst2.save()
		
		self.study1 = Study(
			user=self.user2,
			title='Effects of Smoking',
			institution=self.inst1,
			irb_number='421',
			irb_proposal=settings.MEDIA_ROOT+'/somefile1',
		)
		
		self.study2 = Study(
			user=self.user2,
			title='Effects of Smoking',
			institution=self.inst1,
			irb_number='421',
			irb_proposal=settings.MEDIA_ROOT+'/somefile2',
		)
	
