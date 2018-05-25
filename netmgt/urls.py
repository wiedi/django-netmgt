from django.urls import include, path
import netmgt.export as export

urlpatterns = [
	path('export/zones.zip', export.export),
	path('export/zones.txt', export.text),
]
