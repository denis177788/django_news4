from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
 # path('pages/', include('django.contrib.flatpages.urls')),
   path('news/', include('news.urls')),
   path('articles/', include('news.urls1')),
]