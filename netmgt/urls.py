from django.conf.urls import patterns
import export

urlpatterns = patterns('',
	(r'^export/zones.zip', export.export),
	(r'^export/zones.txt', export.text),
)
