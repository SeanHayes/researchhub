#Django imports
from django.conf.urls.defaults import *

#App imports
from views import index, study_list

# place app url patterns here
urlpatterns = patterns('',
	url(r'^$', index, name="researchhub_app_index"),
	url(r'^studies/$', study_list, name="researchhub_app_study_list"),
)
