#Python imports
from datetime import date

#Django imports
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

#App imports
from ..models import Study, SubjectProfile
from ..views import no_profile_msg, no_studies_msg, profile_successfully_edited_msg

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
		self.study1.earliest_birthdate = date(year=1985, month=1, day=1)
		self.study1.latest_birthdate = date(year=1985, month=12, day=30)
		self.study1.save()
		self.study2.status = Study.STATUS_PUBLISHED
		self.study2.earliest_birthdate = date(year=1985, month=1, day=1)
		self.study2.latest_birthdate = date(year=1985, month=12, day=30)
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

class SubjectProfileTestCase(BaseTestCase):
	def test_get_logged_out(self):
		url = reverse('researchhub_app_profile_edit')
		response = self.client.get(url, follow=True)
		
		self.assertRedirects(response, '/accounts/login/?next='+url)
	
	def test_get_logged_in(self):
		self.client.login(username=self.username, password=self.password)
		
		response = self.client.get(reverse('researchhub_app_profile_edit'))
		
		self.assertEqual(response.status_code, 200)
	
	def test_post_logged_in_bad_data_fail(self):
		self.client.login(username=self.username, password=self.password)
		
		post_data = {
			
		}
		
		response = self.client.post(reverse('researchhub_app_profile_edit'), post_data)
		
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, profile_successfully_edited_msg)
	
	def test_post_logged_create_profile_success(self):
		post_data = {
			'birthdate': date.today().isoformat(),
			'gender': SubjectProfile.GENDER_MALE,
			'city': 'Rochester',
			'state': 'NY',
			'postal_code': '14607',
			'country': 'US',
		}
		
		self.client.login(username=self.username, password=self.password)
		
		self.profile1.delete()
		
		user = User.objects.get(id=self.user1.id)
		self.assertRaises(SubjectProfile.DoesNotExist, lambda: user.subjectprofile)
		
		response = self.client.post(reverse('researchhub_app_profile_edit'), post_data, follow=True)
		
		user = User.objects.get(id=self.user1.id)
		profile = user.subjectprofile
		
		self.assertEqual(profile.postal_code, post_data['postal_code'])
		
		self.assertRedirects(response, reverse('researchhub_app_study_list'))
		self.assertContains(response, profile_successfully_edited_msg)
	
	def test_post_logged_edit_profile_success(self):
		post_data = {
			'birthdate': date.today().isoformat(),
			'gender': SubjectProfile.GENDER_MALE,
			'city': 'Rochester',
			'state': 'NY',
			'postal_code': '14607',
			'country': 'US',
		}
		
		self.client.login(username=self.username, password=self.password)
		
		user = User.objects.get(id=self.user1.id)
		profile = user.subjectprofile
		
		self.assertNotEqual(profile.postal_code, post_data['postal_code'])
		
		response = self.client.post(reverse('researchhub_app_profile_edit'), post_data, follow=True)
		
		user = User.objects.get(id=self.user1.id)
		profile = user.subjectprofile
		
		self.assertEqual(profile.postal_code, post_data['postal_code'])
		
		self.assertRedirects(response, reverse('researchhub_app_study_list'))
		self.assertContains(response, profile_successfully_edited_msg)
	
