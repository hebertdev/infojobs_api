from rest_framework import  viewsets, status
from rest_framework.response import Response
import requests
from apps.users.models import User
from api.authentication import get_candidate_data 
#serializers
from api.infojobs.serializers.infojobs import InfojobsAuthenticationSerializer
from decouple import config

class InfojobsAuthenticationView(viewsets.ViewSet):
    def create(self, request):
        serializer = InfojobsAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if 'code' not in serializer.validated_data:
            return Response({'error': 'The code is required'}, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data['code']

        # Make the POST request
        token_url = config('TOKEN_URL', default=False, cast=str)
        client_id = config('CLIENT_ID', default=False, cast=str)
        client_secret = config('CLIENT_SECRET', default=False, cast=str)
        redirect_uri = config('REDIRECT_UI', default=False, cast=str)

        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }

        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            response_data = response.json()

            access_token = response_data.get('access_token')
            if access_token:
                candidate_data = get_candidate_data(access_token)
                # Get candidate information
                infojobs_id = candidate_data.get('id')

                # Check if the user already exists by infojobs_id
                user, created = User.objects.get_or_create(infojobs_id=infojobs_id)

                # Update user data
                user.username = str(candidate_data.get('id')) or user.username
                user.email = candidate_data.get('email') or user.email
                user.first_name = candidate_data.get('name') or user.first_name
                user.last_name = candidate_data.get('surname1') or user.last_name
                user.save()
                result = {
                    'tokens': response_data,
                    'candidate_data': candidate_data,
                    'user_created': created,
                    'user_id': user.id
                }
                return Response(result)
            else:
                return Response({'error': 'Failed to obtain access token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            # Handle request errors
            return Response({'error': 'Error in POST request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValueError:
            # Handle JSON decoding errors
            return Response({'error': 'Error decoding JSON response'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




       
        
