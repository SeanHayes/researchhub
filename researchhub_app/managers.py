#Python imports
import logging

#Django imports
from django.db import models
from django.db.models import Q

logger = logging.getLogger(__name__)

# Create your managers here.

class StudyManager(models.Manager):
	def get_for_user(self, user, researchprofile):
		
		criteria_args = (
			Q(earliest_birthdate__isnull= True,) | Q(earliest_birthdate__lte=researchprofile.birthdate,),
			Q(latest_birthdate__isnull= True,) | Q(latest_birthdate__gte=researchprofile.birthdate,),
			Q(gender__isnull= True,) | Q(gender=researchprofile.gender,),
		)
		
		criteria_kwargs = {
			'status': self.model.STATUS_PUBLISHED,
		}
		
		
		return self.filter(*criteria_args, **criteria_kwargs)

