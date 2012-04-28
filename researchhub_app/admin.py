#Python imports
import logging

#Django imports
from django.contrib import admin

#App imports
from models import Study, SubjectProfile

logger = logging.getLogger(__name__)

admin.site.register(Study)
admin.site.register(SubjectProfile)

