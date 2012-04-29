#Python imports
from datetime import datetime, timedelta

#Django imports
from django.utils.timezone import utc

def get_utc_datetime(**offsets):
	dt = datetime.utcnow().replace(tzinfo=utc)
	if offsets:
		dt = dt + timedelta(**offsets)
	return dt

