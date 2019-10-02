"""GoShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views

from GoShop import settings
from rest_framework_swagger.views import get_swagger_view
# from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from GoShop.views import obtain_expiring_auth_token

schema_view = get_swagger_view(title="API文档")

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api-computer/', include('computerapps.urls')),
    re_path(r'^api-token-auth/', views.obtain_auth_token),
#    re_path(r'^api-auth/', include('rest_framework.urls'), name='rest_framework'),
#    re_path(r'^api-token/', obtain_expiring_auth_token, name='api-token'),
    path('api-docs/', schema_view, name="API文档"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
