from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from deck import urls as deck_urls
from deck import api_urls
from authentication import urls as authentication_urls

urlpatterns = [
   url(r'^admin/manager/customuser/(?P<pk>\d+)/change/password/$', RedirectView.as_view(url='/admin/manager/customuser/(?P<pk>\d+)/', permanent=False), name='index'),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^rest-auth/', include('rest_auth.urls')),
   url(r'^deck/v2/auth/', include('rest_framework.urls', namespace='rest_framework')),
   url(r'^deck/v2', include(api_urls, namespace='deck_api')),  
   url('^searchableselect/', include('searchableselect.urls')),
   url(r'^deck/', include(deck_urls, namespace="deck")),
   url(r'^accounts/', include(authentication_urls, namespace="auth")),
]
