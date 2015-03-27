from django.test import TestCase
from django.conf import settings

class HoursServiceTestCase(TestCase):

	def test_get_entries(self):
		
		url = '{0}/api/v1/entry/' . format(settings.HOURSSERVICE_BASE_URL)

		response = self.client.get(url, content_type='application/json')
		
		#assert response.status_code == 200, 'Expect 200 OK'
		#assert response.json().get("username") == "admin", 'Expect the current user to be returned'

