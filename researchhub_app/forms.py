#Python imports
import logging

#Django imports
from django import forms

#App imports
from models import SubjectProfile

logger = logging.getLogger(__name__)

# place form definitions here
class SubjectProfileForm(forms.ModelForm):
	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(SubjectProfileForm, self).__init__(*args, **kwargs)
	
	def clean(self):
		cleaned_data = self.cleaned_data
		
		self.instance.user = self.user
		
		return cleaned_data
	
	class Meta:
		model = SubjectProfile
		exclude = ('user',)
