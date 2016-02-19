from django.contrib.auth import authenticate, login

class ConsumerMiddleware(object):  
	"""
	Get the user credentials from the Kong headers:

		X-Consumer-ID, the ID of the Consumer on Kong
		X-Consumer-Custom-ID, the custom_id of the Consumer (if set)
		X-Consumer-Username, the username of the Consumer (if set)
	"""
    def process_request(self, request):  

        username = request.META.get('X-Consumer-Username', None)
        id = request.META.get('X-Consumer-Custom-ID', None)

        if not token is None:
        	try: 
        		user = User.objects.get(username=username)
        	except User.DoesNotExist:
        		user = User.objects.create(username=user, id=id)
	        
	        login(request, user)
	                
        return None            
            
