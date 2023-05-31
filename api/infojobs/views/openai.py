# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decouple import config
import openai
from api.infojobs.serializers.openai import AnalizeSerializer
from api.authentication import InfojobsAuthentication
import json

openai.api_key = config('OPENAI_KEY', default=False, cast=str)

class AnalizeViewSet(viewsets.ViewSet):
    authentication_classes = [InfojobsAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = AnalizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        texto = serializer.validated_data['texto']

        json_data = json.loads(texto)
        texto_string = json.dumps(json_data)

        context = [
            {'role': 'system', 'content': """
            Quiero que, 
            cuando te envíe una OFERTA DE EMPLEO junto con mi CV en formato JSON,
            actues como un reclutador experto en la industria de la empresa y si la industria no esta en la oferta actúes como un reclutador general,
            y analices la compatibilidad entre mi cv y la oferta. 
            A continuación, asigna una puntuación del 1 al 10 según tus criterios de análisis,  si el puesto de la oferta no tiene nada que ver con mi carrera o skills ponme una nota super baja de 2 a 3. 
            Sé consico, extrico y directo, expresa tu respuesta como asistente hacia mi persona. 
            Selecciona habilidades faltantes de mi persona y muestra una lista de las mismas. 
            Además,
            proporciona una lista de consultas de búsqueda en YouTube para la lista de habilidades faltantes. 
            Por último, para "respuesta_asistente" y  "recomendacion_general" tienes 400 caracteres como máximox, devuelve el análisis en formato JSON, excluyendo cualquier comentario adicional. Aquí tienes un ejemplo de cómo debe ser la estructura de respuesta en formato JSON
            {
                "respuesta_asistente": String,
                "puntuacion_compatibilidad": Number,
                "habilidades_faltantes": String[],
                "recomendacion_general": String,
                "youtube_queries": String[]
            } """},
            {'role': 'user', 'content': texto_string}
        ]

        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=context
        )

        rpta = json.loads(respuesta.choices[0].message["content"])
        return Response({'respuesta': rpta})
