"""suba_safe_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Imports de Django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# Imports de DRF
from rest_framework import permissions

# Imports de DRF-YASG
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Suba Safe API",
      default_version='v2',
      description="Documentación de la API de Suba Safe",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="alex-patricio1999@hotmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Urls de DRF-YASG
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('', include('applications.users.urls')),
    path('', include('applications.article.urls')),
    path('', include('applications.auction.urls')),
    path('', include('applications.payment.urls')),
    # path('', include('applications.bid.urls')),
    # path('', include('applications.category.urls')),
    path('', include('applications.comment.urls')),

    # Routers del ViewSet
    path('', include('applications.users.routers')),
    path('', include('applications.category.routers')),
    path('', include('applications.article.routers')),
    path('', include('applications.bid.routers')),
    path('', include('applications.auction.routers')), 
    path('', include('applications.payment.routers')), 
    path('', include('applications.comment.routers')), 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
