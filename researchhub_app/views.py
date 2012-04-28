#Python imports
import logging

#django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render

#App imports
from models import Study, SubjectProfile

logger = logging.getLogger(__name__)

# Create your views here.

no_profile_msg = 'Please fill out a profile in order to qualify for research studies.'
no_studies_msg = 'There are no research studies available to you at this time.'

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



