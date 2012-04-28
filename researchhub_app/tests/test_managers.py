#Python imports
from datetime import datetime

#App imports
from ..models import Study, SubjectProfile

#Test imports
from util import BaseTestCase

class StudyManagerTestCase(BaseTestCase):
	def test_get_for_user_no_studies_published(self):
		self.study1.status = Study.STATUS_DRAFT
		self.study1.save()
		self.study2.status = Study.STATUS_DRAFT
		self.study2.save()
		
		user = self.user1
		profile = user.subjectprofile
		studies = Study.objects.get_for_user(user, profile)
		
		self.assertEqual(len(studies), 0)
	
	def test_get_for_user_birthdate_not_in_range(self):
		self.study1.status = Study.STATUS_PUBLISHED
		self.study1.earliest_birthdate = datetime(year=1985, month=1, day=1)
		self.study1.latest_birthdate = datetime(year=1985, month=12, day=30)
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.earliest_birthdate = datetime(year=1985, month=1, day=1)
		self.study2.latest_birthdate = datetime(year=1985, month=12, day=30)
		self.study2.save()
		
		user = self.user1
		profile = user.subjectprofile
		studies = Study.objects.get_for_user(user, profile)
		
		self.assertEqual(len(studies), 0)
	
	def test_get_for_user_birthdate_is_in_range(self):
		self.study1.status = Study.STATUS_PUBLISHED
		self.study1.earliest_birthdate = datetime(year=1986, month=1, day=1)
		self.study1.latest_birthdate = datetime(year=1986, month=12, day=30)
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.earliest_birthdate = datetime(year=1986, month=1, day=1)
		self.study2.latest_birthdate = datetime(year=1986, month=12, day=30)
		self.study2.save()
		
		user = self.user1
		profile = user.subjectprofile
		studies = Study.objects.get_for_user(user, profile)
		
		self.assertEqual(len(studies), 2)
		self.assertEqual(studies[0].id, self.study2.id)
		self.assertEqual(studies[1].id, self.study1.id)
	
	def test_get_for_user_no_birthdate_specified(self):
		self.study1.status = Study.STATUS_PUBLISHED
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.save()
		
		user = self.user1
		profile = user.subjectprofile
		studies = Study.objects.get_for_user(user, profile)
		
		self.assertEqual(len(studies), 2)
		self.assertEqual(studies[0].id, self.study2.id)
		self.assertEqual(studies[1].id, self.study1.id)
	
	def test_get_for_user_gender_matches(self):
		self.study1.status = Study.STATUS_PUBLISHED
		self.study1.gender = SubjectProfile.GENDER_MALE
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.gender = SubjectProfile.GENDER_FEMALE
		self.study2.save()
		
		user = self.user1
		profile = user.subjectprofile
		studies = Study.objects.get_for_user(user, profile)
		
		self.assertEqual(len(studies), 1)
		self.assertEqual(studies[0].id, self.study1.id)
	
	def test_get_for_user_birthdate_and_gender_match(self):
		self.study1.status = Study.STATUS_PUBLISHED
		self.study1.earliest_birthdate = datetime(year=1986, month=1, day=1)
		self.study1.latest_birthdate = datetime(year=1986, month=12, day=30)
		self.study1.gender = SubjectProfile.GENDER_MALE
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.earliest_birthdate = datetime(year=1986, month=1, day=1)
		self.study2.latest_birthdate = datetime(year=1986, month=12, day=30)
		self.study2.gender = SubjectProfile.GENDER_FEMALE
		self.study2.save()
		
		user = self.user1
		profile = user.subjectprofile
		studies = Study.objects.get_for_user(user, profile)
		
		self.assertEqual(len(studies), 1)
		self.assertEqual(studies[0].id, self.study1.id)

