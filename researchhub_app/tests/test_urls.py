#Python imports
from datetime import datetime

#Django imports
from django.core.urlresolvers import reverse

#App imports
from ..models import Study
from ..views import no_profile_msg, no_studies_msg

#Test imports
from util import BaseTestCase

class IndexTestCase(BaseTestCase):
	def test_get(self):
		response = self.client.get(reverse('researchhub_app_index'))
		
		self.assertEqual(response.status_code, 200)

class StudyListTestCase(BaseTestCase):
	def test_get_logged_out(self):
		url = reverse('researchhub_app_study_list')
		response = self.client.get(url, follow=True)
		
		self.assertRedirects(response, '/accounts/login/?next='+url)
	
	def test_get_logged_in_no_studies(self):
		self.client.login(username=self.username, password=self.password)
		
		response = self.client.get(reverse('researchhub_app_study_list'))
		
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, no_profile_msg)
		self.assertContains(response, no_studies_msg)
		self.assertNotContains(response, self.study1.title)
		self.assertNotContains(response, self.study2.title)
	
	def test_get_logged_in_with_no_published_studies(self):
		self.study1.save()
		self.study2.save()
		
		self.client.login(username=self.username, password=self.password)
		
		response = self.client.get(reverse('researchhub_app_study_list'))
		
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, no_profile_msg)
		self.assertContains(response, no_studies_msg)
		self.assertNotContains(response, self.study1.title)
		self.assertNotContains(response, self.study2.title)
	
	def test_get_logged_in_user_has_no_profile(self):
		self.user1.subjectprofile.delete()
		
		self.study1.status = Study.STATUS_PUBLISHED
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.save()
		
		self.client.login(username=self.username, password=self.password)
		
		response = self.client.get(reverse('researchhub_app_study_list'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, no_profile_msg)
		self.assertContains(response, no_studies_msg)
		self.assertNotContains(response, self.study1.title)
		self.assertNotContains(response, self.study2.title)
	
	def test_get_logged_in_with_no_qualifying_studies(self):
		self.study1.status = Study.STATUS_PUBLISHED
		self.study1.earliest_birthdate = datetime(year=1985, month=1, day=1)
		self.study1.latest_birthdate = datetime(year=1985, month=12, day=30)
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.earliest_birthdate = datetime(year=1985, month=1, day=1)
		self.study2.latest_birthdate = datetime(year=1985, month=12, day=30)
		self.study2.save()
		
		self.client.login(username=self.username, password=self.password)
		
		response = self.client.get(reverse('researchhub_app_study_list'), follow=True)
		
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, no_profile_msg)
		self.assertContains(response, no_studies_msg)
		self.assertNotContains(response, self.study1.title)
		self.assertNotContains(response, self.study2.title)
	
	def test_get_logged_in_with_available_studies(self):
		self.study1.status = Study.STATUS_PUBLISHED
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.save()
		
		self.client.login(username=self.username, password=self.password)
		
		response = self.client.get(reverse('researchhub_app_study_list'))
		
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, no_profile_msg)
		self.assertNotContains(response, no_studies_msg)
		self.assertContains(response, self.study1.title)
		self.assertContains(response, self.study2.title)
	
