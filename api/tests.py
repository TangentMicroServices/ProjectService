from django.test import TestCase, Client
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import User
from api.models import Project, Task, Resource

from  datetime import date

import requests 
import responses
import json


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

		self.joe_admin = User.objects.create_superuser(username="admin", password="test", email="joe@soap.com")
		self.joe_soap = User.objects.create_user(username="joe", password="test")
		self.joe_soap.save()

		## setup a bunch of Projects
		p1 = Project.quick_create(title="P1", description="Search me", is_billable=True)
		p2 = Project.quick_create(title="P2", is_billable=True)
		p3 = Project.quick_create(title="P3", is_active=False)
		p4 = Project.quick_create(title="P4", user=self.joe_soap.pk, description="Search me too")
		p5 = Project.quick_create(title="P5", user=self.joe_soap.pk)
		p6 = Project.quick_create(title="P6")

		Resource.quick_create(user=self.joe_soap.pk, project=p4)
		Resource.quick_create(user=self.joe_soap.pk, project=p3)

		Resource.quick_create(user=self.joe_admin.pk, project=p1)
		Resource.quick_create(user=self.joe_admin.pk, project=p2)


	@responses.activate
	def test_get_projects_list_returns_empty_list_if_no_user_is_specified(self):

		response = self.c.get("/projects/")			
		assert response.status_code == 200
		assert len(response.json()) == 0

	@responses.activate
	def test_get_project_list(self):

		self.c.login(username="joe", password="test")
		#self.c.logout()
		#login_result = self.c.login(username="joe", password="test")

		response = self.c.get("/projects/")

		assert response.status_code == 200, 'Expect 200 OK'
		assert len(response.json()) == 2, 'Expect 2 projects back'

	@responses.activate
	def test_get_project_list_admin_gets_all_projects(self):

		self.c.login(username="admin", password="test")
		#self.c.logout()
		#login_result = self.c.login(username="joe", password="test")

		response = self.c.get("/projects/")

		assert response.status_code == 200, 'Expect 200 OK'
		assert len(response.json()) == 6, 'Expect 6 projects back'

	@responses.activate
	def test_get_project_list_filter_on_active(self):

		self.c.login(username="joe", password="test")
		response = self.c.get("/projects/?is_active=False")

		for project in response.json(): 
			assert project.get("is_active") == False, \
				'Assert that not proejcts are returned with is_active = True. But: {} returned True' . format (project)
		

	@responses.activate
	def test_get_project_list_filter_on_billable(self):

		self.c.login(username="joe", password="test")
		response = self.c.get("/projects/?is_billable=True")

		for project in response.json(): 
			assert project.get("is_active") == False, \
				'Assert that not proejcts are returned with is_billable= False. But: {} returned False' . format (project)
		

	@responses.activate
	def test_get_project_list_search_title(self):
		"""Admin can search all projects by title"""

		self.c.login(username="admin", password="test")
		response = self.c.get("/projects/?search=P1")

		titles = [project.get("title") for project in response.json()]
		expected_titles = ['P1'] 
		assert titles == expected_titles, 'Expect search to return matching title'

	@responses.activate
	def test_get_project_list_search_description(self):
		"""User can search their projects by description"""

		self.c.login(username="joe", password="test")
		response = self.c.get("/projects/?search=Search")

		titles = [project.get("title") for project in response.json()]
		expected_titles = ['P4'] # user only gets their own projects
		
		assert titles == expected_titles, 'Expected {}. Got: {}' . format (expected_titles, titles)

	def test_get_project_list_user_search_description(self):
		"""Admin can search all projects by description"""

		self.c.login(username="admin", password="test")
		response = self.c.get("/projects/?search=Search&ordering=title")

		titles = [project.get("title") for project in response.json()]
		expected_titles = ['P1', 'P4'] 
		assert titles == expected_titles, 'Expected {}. Got: {}' . format (expected_titles, titles)


	@responses.activate
	def test_get_project_orders_by_title(self):

		self.c.login(username="admin", password="test")
		response = self.c.get("/projects/?ordering=title")

		titles = [project.get("title") for project in response.json()]
		expected_titles = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'] 
		
		assert titles == expected_titles, 'Expect search results ordered by title'


	@responses.activate
	def test_get_project_user_gets_own_projects(self):
		"""A user should only see projects in which they are staffed"""

		normal_user = User.objects.get(username="joe")

		project = Project.quick_create()
		project2 = Project.quick_create()

		resource = Resource.quick_create(project=project, user=normal_user.pk)

		self.c.login(username=normal_user.username, password="test")

		response = self.c.get("/projects/{0}/" . format (project.pk))		
		assert response.status_code == 200, 'Expect 200 OK'
		
		# todo: 
		# put a proper assertion in here.

class KongConsumerMiddlewareTestCase(TestCase):

	def setUp(self):
		self.c = Client()
		self.user = User.objects.create_user(username="joe", password="test")

		Project.quick_create(user=self.user.pk)


	def test_user_is_logged_in(self):
		
		
		headers = {
			'X-Consumer-Custom-ID':self.user.pk, 
			'X-Consumer-Username':self.user.username}
		c = Client(**headers)
		
		response = c.get("/projects/", **headers)



		






