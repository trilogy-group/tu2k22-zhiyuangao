"""tu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .routers import router
from . import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log/', api_views.logtest),
    path('api/v1/auth/signup/', api_views.register),
    path('api/v1/auth/login/', api_views.login),
    path('api/v1/auth/logout/', api_views.logout),
    path('api/v1/auth/githublogin/', api_views.githublogin),
    path('api/v1/users/profile/', api_views.profile),
    path('api/v1/sectors/', api_views.sectors),
    path('api/v1/sectors/<int:id>/', api_views.sectorsUpdate),
    path('api/v1/stocks/', api_views.stocks),
    path('api/v1/stocks/<int:id>/', api_views.getStockById),
    path('api/v1/orders/', api_views.orders),
    path('api/v1/orders/match/', api_views.match),
    path('api/v1/process-logs/', api_views.processlogs),
    path('api/v1/recommend/', api_views.recommend),
    path('api/v1/emailurl/', api_views.emailurl),
    path('api/v1/market/open/', api_views.open),
    path('api/v1/market/close/', api_views.close),
    path('api/v1/market/ohlc/', api_views.ohlc),
    path('api/v1/holdings/', api_views.holdings),
    path('news/<str:p>/', api_views.fetch),
    path('api/', include(router.urls)),
    path('', include('django_prometheus.urls')),
]

#if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
