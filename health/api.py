from rest_framework import routers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.models import User

@api_view(['GET'])
@permission_classes((AllowAny,))
def health(request):

	# make sure the db is there.
	User.objects.first()
	json = {
		'name': "ProjectService",
		'status': 'up',
		'info': {
			'explorer': '/explorer',
			'api': '/',
			'health': '.. well, you\'re here right?'
		}
	}

	return Response(json)