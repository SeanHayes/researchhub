
from django.conf import settings
from django.conf.urls import patterns, include, url
import logging
import sys

logger = logging.getLogger(__name__)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^', include('researchhub_app.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	(r'^accounts/', include('registration.urls')),
)

#only active when runserver is used
if 'runserver' in sys.argv or 'runserver_plus' in sys.argv:
	urlpatterns += patterns('',
		(r'^'+settings.MEDIA_URL[1:]+'(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)

