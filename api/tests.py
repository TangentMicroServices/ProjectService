from django.test import TestCase, Client
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Project, Task, Resource

from tokenauth.authbackends import TokenAuthBackend
from  datetime import date

import requests 
import responses
import json


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

	def test_project_unicode(self):
		project = Project.quick_create(title="Test")
		assert project.__unicode__() == 'Test'


	def test_quick_create(self):
		project = Project.quick_create()
		
		assert isinstance(project, Project), 'Project instance is created'


class ResourceModelTestCase(TestCase):

	def test_resource_quick_create(self):
		resource = Resource.quick_create()

		assert isinstance(resource, Resource)

	def test_resource_quick_create_with_details(self):
		project = Project.quick_create(title="TEST")
		extra_data = {
			"rate": 100
		}
		resource = Resource.quick_create(project=project, **extra_data)

		assert resource.project.title == 'TEST', 'Expect project is explicitly set'
		assert resource.rate == 100.00, 'Expect rate to be set by kwargs'
	
	def test_project_user_unique_together(self):
		project = Project.quick_create()
		start_date = date.today()
		Resource.objects.create(project=project, user=1, start_date=start_date)
		Resource.objects.create(project=project, user=2, start_date=start_date)

		try:
			Resource.objects.create(project=project, user=2)
			self.fail("Should not be able to add the same project and user twice")
		except IntegrityError:
			pass

class TaskModelTestCase(TestCase):

	def test_quick_create(self):
		task = Task.quick_create()
		
		assert isinstance(task, Task), 'Task instance is created'


class ProjectEndpointTestCase(TestCase):

	def setUp(self):
		self.c = Client(Authorization='Token 123')

		## setup a bunch of Projects
		Project.quick_create(title="P1", description="Search me", is_billable=True)
		Project.quick_create(title="P2", is_billable=True)
		Project.quick_create(title="P3", is_active=False)
		Project.quick_create(title="P4", user=2)
		Project.quick_create(title="P5", user=2)
		Project.quick_create(title="P6")

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
	def test_get_project_list_filter_on_active(self):

		mock_auth_success()
		response = self.c.get("/api/v1/projects/?is_active=False")

		titles = [project.get("title") for project in json.loads(response.content)]
		expected_titles = ['P3'] 
		assert titles == expected_titles, 'Expect results to be filtered on is_active=False'

	@responses.activate
	def test_get_project_list_filter_on_billable(self):

		mock_auth_success()
		response = self.c.get("/api/v1/projects/?is_billable=True")

		titles = [project.get("title") for project in json.loads(response.content)]
		expected_titles = ['P1', 'P2'] 
		assert titles == expected_titles, 'Expect results to be filtered on is_billable=True'

	@responses.activate
	def test_get_project_list_search_title(self):

		mock_auth_success()
		response = self.c.get("/api/v1/projects/?search=P1")

		titles = [project.get("title") for project in json.loads(response.content)]
		expected_titles = ['P1'] 
		assert titles == expected_titles, 'Expect search to return matching title'

	@responses.activate
	def test_get_project_list_search_description(self):

		mock_auth_success()
		response = self.c.get("/api/v1/projects/?search=Search")

		titles = [project.get("title") for project in json.loads(response.content)]
		expected_titles = ['P1'] 
		assert titles == expected_titles, 'Expect search to return matching description'

	@responses.activate
	def test_get_project_orders_by_title(self):

		mock_auth_success()
		response = self.c.get("/api/v1/projects/?ordering=title")

		titles = [project.get("title") for project in json.loads(response.content)]
		expected_titles = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'] 
		assert titles == expected_titles, 'Expect search results ordered by title'


	@responses.activate
	def test_get_project(self):

		project = Project.quick_create()
		mock_auth_success()

		response = self.c.get("/api/v1/projects/{0}/" . format (project.pk))

		expected_fields = ['pk', 'title', 'description', 'start_date', 'end_date', 'is_billable', 'is_active', 'task_set', 'resource_set']

		for field in expected_fields:
			assert response.data.get(field, "NOTSET") != "NOTSET", 'Assert field {0} is returned in the response' . format (field)

		assert response.status_code == 200, 'Expect 200 OK'

class TaskEndpointTestCase(TestCase):

	def setUp(self):
		self.c = Client(Authorization='Token 123')

		# create some Tasks






