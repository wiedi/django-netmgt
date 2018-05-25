from django.urls import include, path
from django.contrib import admin

admin.site.site_header = 'Network Management Tool'
admin.autodiscover()

urlpatterns = [
	path('netmgt/', include('netmgt.urls')),
	path('admin/', admin.site.urls),
]
