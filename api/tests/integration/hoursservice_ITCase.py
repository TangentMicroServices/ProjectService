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

class HoursServiceTestCase(TestCase):

	def test_get_entries(self):
		
		mock_auth_success()
		url = '{0}/api/v1/entry/' . format(settings.HOURSSERVICE_BASE_URL)

		response = self.client.get(url, content_type='application/json')
		
		assert response.status_code == 200, 'Expect 200 OK'
		#assert response.json().get("username") == "admin", 'Expect the current user to be returned'

