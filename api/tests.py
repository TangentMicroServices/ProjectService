from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from .models import Project, Task

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

class ProjectModelTestCase(TestCase):

	def test_quick_create(self):
		project = Project.quick_create()
		
		assert isinstance(project, Project), 'Project instance is created'


class TaskModelTestCase(TestCase):

	def test_quick_create(self):
		task = Task.quick_create()
		
		assert isinstance(task, Task), 'Task instance is created'


class ProjectEndpointTestCase(TestCase):

	def setUp(self):
		self.c = Client(Authorization='Token 123')

	@responses.activate
	def test_get_projects_list_requires_auth(self):

		mock_auth_failure()
		response = self.c.get("/api/v1/projects/")			
		assert response.status_code == 403, 'Expect permission denied'

	@responses.activate
	def test_get_project_list(self):

		mock_auth_success()

		response = self.c.get("/api/v1/projects/")

		assert response.status_code == 200, 'Expect 200 OK'

	@responses.activate
	def test_get_project(self):

		project = Project.quick_create()
		mock_auth_success()

		response = self.c.get("/api/v1/projects/{0}/" . format (project.pk))

		expected_fields = ['title', 'description', 'start_date', 'end_date', 'is_billable', 'is_active', 'task_set',]

		for field in expected_fields:
			assert response.data.get(field, "NOTSET") != "NOTSET", 'Assert field {0} is returned in the response' . format (field)

		assert response.status_code == 200, 'Expect 200 OK'

class TaskEndpointTestCase(TestCase):

	def setUp(self):
		self.c = Client(Authorization='Token 123')

		# create some Tasks






