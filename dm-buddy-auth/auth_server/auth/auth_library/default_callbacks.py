
import json



def default_invalid_token_callback(error_string = 'Invalid Token'):
	"""
	Default method that is passed if a protected resource is accessed with an invalid token. Error string is returned to the function with a 401 status code

	:param error_string: A string that explains why this request is unauthorized
	"""

	return {'message':error_string, 'status':'fail'}, 401

def default_unauthorized_callback(error_string = 'Unauthorized'):
	"""
	Default method that is passed if a protected resource is accessed without a token. Error string is returned to the function with a 401 status code

	:param error_string: A string that explains why this request is unauthorized
	"""

	return {'message':error_string, 'status':'fail'}, 401

def default_needs_fresh_token_calback():
	"""
	Default method that is passed if an expired access token is used to access a protected resource,

	return a message that details Refresh is required with a 401 status code.
	"""

	return {'message':'Refresh Required', 'status':'fail'}, 401

def protected_access_resource(auth_token, authorized_callback, unauthorized_callback = default_unauthorized_callback('Unauthorized')):
	"""
	Method used to protect a resource. This is used in a view to determine whether they are authorized or unauthorized. User passes an access token and the method handles all of the responses

	:param auth_token: Token the user is attempting to authorized with. 
	:param authorized_callback: This is a callback method we used to return a json string to the view to be presented. The callback method should be part of the view class as a staticmethod.
	:param unauthorized_callback: If there is still information that we want to present if the token is not authorized we can pass a callback method here.
	"""

	# If a valid auth_token is present
	if auth_token:
		auth_token = auth_token.split(" ")[1]
		resp = User.decode_token(auth_token, 'access')

		#when decoding the token, if the response is not a string, else we have an error and pass it to the default_expired_token_callback
		if not isinstance(resp, str):
			return authorized_callback
		elif resp == 'Expired':
			return default_needs_fresh_token
		return unauthorized_callback
	else:
		return unauthorized_callback
