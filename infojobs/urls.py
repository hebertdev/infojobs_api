from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('api.infojobs.urls' , 'infojobs') , namespace="infojobs")),
    path('api/', include(('api.users.urls', 'users_api'), namespace="users_api")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
