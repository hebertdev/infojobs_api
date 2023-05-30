from rest_framework.exceptions import AuthenticationFailed
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from apps.users.models import User
import requests
from PIL import Image
import io
from decouple import config


def get_candidate_data(access_token):
    url = 'https://api.infojobs.net/api/6/candidate'
    basic_token = config('BASIC_TOKEN', default=False, cast=str)
    total_token = 'Basic ' + basic_token + ', Bearer ' + access_token
    headers = {
        'Authorization': total_token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data

class InfojobsAuthentication(OAuth2Authentication):
    def authenticate(self, request):
        print('estás entrando a la autenticación')
        # Obtener el token de acceso del encabezado de autorización
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # No se proporcionó el token de acceso

        access_token = auth_header.split(' ')[1]

        # Lógica adicional para autenticar al usuario basado en el token de acceso de Infojobs
        try:
            candidate_data = get_candidate_data(access_token)
            # Verificar si el candidato ya existe en tu base de datos
            infojobs_id = candidate_data.get('id')
            user = User.objects.get(infojobs_id=infojobs_id)
            
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid access token')
        except Exception as e:
            raise AuthenticationFailed('Invalid access token')

        return (user,  candidate_data)