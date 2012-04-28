#Python imports
import logging

#django imports
from django.shortcuts import render

logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
	return render(request, 'researchhub_app/index.html')
