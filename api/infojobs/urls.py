# core/urls.py
from django.urls import path, include

# djangorf
from rest_framework.routers import DefaultRouter
from .views import infojobs , openai


router = DefaultRouter()
router.register(r'autenticacion',infojobs.InfojobsAuthenticationView, basename="autenticacion")
router.register(r'analize',openai.AnalizeViewSet, basename="analizeview")

urlpatterns = [
    path('', include(router.urls)),
]