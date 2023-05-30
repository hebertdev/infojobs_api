from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

class AuthenticationFailedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except AuthenticationFailed as e:
            response = Response({'error': str(e)}, status=401)
        return response