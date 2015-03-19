from django.test import TestCase, Client
from django.conf import settings

import requests 
import responses


class HealthTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()

	def test_health_returns_useful_information(self):

		response = self.client.get('/health/')
    
        assert response.status_code == 200, 'Expect 200 OK'
        self.assertEqual(response.data, {"name": "ProjectService", "explorer_url": "/api-explorer/","version": settings.VERSION})