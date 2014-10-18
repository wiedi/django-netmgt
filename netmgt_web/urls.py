from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.site.site_header = 'Network Management Tool'
admin.autodiscover()

urlpatterns = patterns('',
	(r'^netmgt/', include('netmgt.urls')),
	(r'^admin/', include(admin.site.urls)),
)
