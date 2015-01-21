from django.conf.urls import patterns, include, url
from django.contrib import admin
from event_service.views import EventsList, EventByHost

urlpatterns = patterns('',

   url(r'^api/v1.0/(?P<org>[^/]+)/events/?$',
       EventsList.as_view(), name='events'),
   url(r'^api/v1.0/(?P<org>[^/]+)/events/(?P<host_id>[^/]+)/?$',
       EventByHost.as_view(), name='events_by_host'),


   url(r'^admin/', include(admin.site.urls)),
)
