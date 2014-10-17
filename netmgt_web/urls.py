from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	(r'^netmgt/', include('netmgt.urls')),
	(r'^admin/', include(admin.site.urls)),
)
