from rest_framework import routers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def health(request):

	json = {
		#'version': settings.VERSION,
		'name': "ProjectService"
	}
	
	return Response(json)