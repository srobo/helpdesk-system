"""helpdesk URL Configuration

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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import DefaultHomeView, SearchView

urlpatterns = [
    path(f"{settings.BASE_PATH}", DefaultHomeView.as_view(), name="home"),
    path(f"{settings.BASE_PATH}search/", SearchView.as_view(), name="search"),
    path(f"{settings.BASE_PATH}admin/", admin.site.urls),
    path(f"{settings.BASE_PATH}auth/", include("allauth.urls")),
    path(f"{settings.BASE_PATH}accounts/", include("accounts.urls", namespace="accounts")),
    path(f"{settings.BASE_PATH}display/", include("display.urls", namespace="display")),
    path(f"{settings.BASE_PATH}teams/", include("teams.urls", namespace="teams")),
    path(f"{settings.BASE_PATH}tickets/", include("tickets.urls", namespace="tickets")),
]
