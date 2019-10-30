from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.site.site_header = 'Network Management Tool'
admin.site.site_title  = 'Network Management Tool'
admin.autodiscover()

urlpatterns = [
	path('netmgt/', include('netmgt.urls')),
	path('admin/', admin.site.urls),
	path('', RedirectView.as_view(url = 'admin/')),
]
