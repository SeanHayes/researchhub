#Python imports
import logging

#Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe

#App imports
from forms import SubjectProfileForm
from models import Study, SubjectProfile

logger = logging.getLogger(__name__)

# Create your views here.

no_profile_msg = mark_safe('Please <a href="/profile/">fill out a profile</a> in order to qualify for research studies.')
no_studies_msg = 'There are no research studies available to you at this time.'
profile_successfully_edited_msg = 'You successfully edited your profile.'

def index(request):
	return render(request, 'researchhub_app/index.html')

@login_required
def study_list(request):
	user = request.user
	profile = None
	studies = []
	try:
		profile = user.subjectprofile
		studies = Study.objects.get_for_user(user, profile)
	except SubjectProfile.DoesNotExist:
		messages.error(request, no_profile_msg)
	
	return render(
		request,
		'researchhub_app/study_list.html',
		{
			'no_studies_msg': no_studies_msg,
			'studies': studies,
		}
	)

@login_required
def profile_edit(request):
	user = request.user
	profile = None
	try:
		profile = user.subjectprofile
	except SubjectProfile.DoesNotExist:
		pass
	
	if request.method == 'POST':
		form = SubjectProfileForm(user, request.POST, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, profile_successfully_edited_msg)
			return HttpResponseRedirect(reverse('researchhub_app_study_list'))
	else:
		form = SubjectProfileForm(user, instance=profile)
	
	return render(
		request,
		'researchhub_app/profile_edit.html',
		{
			'form': form,
		}
	)
