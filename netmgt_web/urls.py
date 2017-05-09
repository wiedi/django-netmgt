from django.conf.urls import include, url
from django.contrib import admin

admin.site.site_header = 'Network Management Tool'
admin.autodiscover()

urlpatterns = [
	url(r'^netmgt/', include('netmgt.urls')),
	url(r'^admin/', include(admin.site.urls)),
]
