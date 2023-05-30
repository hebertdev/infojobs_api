# core/urls.py
from django.urls import path, include

# djangorf
from rest_framework.routers import DefaultRouter
from .views import infojobs



router = DefaultRouter()
router.register(r'autenticacion',infojobs.InfojobsAuthenticationView, basename="autenticacion")

urlpatterns = [
    path('', include(router.urls)),
]