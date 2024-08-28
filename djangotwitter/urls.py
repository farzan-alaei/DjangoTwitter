"""
URL configuration for djangotwitter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import SearchView

from posts.views import TimeLineView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", include("posts.urls")),
    path("profiles/", include("profiles.urls")),
    path("select2/", include("django_select2.urls")),
    path("", TimeLineView.as_view(), name="timeline"),  # Timeline is the home page of project
    path("search/", SearchView.as_view(), name="search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
