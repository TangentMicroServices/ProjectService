from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User

from tokenauth.authbackends import TokenAuthBackend

import requests 
import responses


def mock_auth_success():

	url = '{0}/users/me/' . format(settings.USER_SERVICE_BASE_URL)		
	response_string = '{"username": "TEST"}'
	responses.add(responses.GET, url,
              body=response_string, status=200,
              content_type='application/json')

def mock_auth_failure():

	url = '{0}/users/me/' . format(settings.USER_SERVICE_BASE_URL)		
	responses.add(responses.GET, url,
              body='', status=401,
              content_type='application/json')

class ProjectEndpointTestCase(TestCase):

	def setUp(self):
		self.c = Client(Authorization='Token 123')

	@responses.activate
	def test_get_entry_list_requires_auth(self):

		mock_auth_failure()
		response = self.c.get("/projects/")
		
		assert response.status_code == 403, 'Expect permission denied'

	@responses.activate
	def test_get_entry_list(self):

		mock_auth_success()

		response = self.c.get("/projects/")

		assert response.status_code == 200, 'Expect 200 OK'
