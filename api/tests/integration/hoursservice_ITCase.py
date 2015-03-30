from django.test import TestCase
from django.conf import settings
import requests 
import responses
import json

def mock_auth_success(user=None):

	url = '{0}/api/v1/users/me/' . format(settings.USERSERVICE_BASE_URL)		
	response_string = '{"username": "TEST"}'
	if user is not None:
		response_string = {
						"username": user.username,
						"id": user.pk
						}
		response_string = json.dumps(response_string)
	
	responses.add(responses.GET, url, body=response_string, status=200, content_type='application/json')
