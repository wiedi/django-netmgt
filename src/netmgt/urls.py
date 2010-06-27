from django.conf.urls.defaults import *
import export

urlpatterns = patterns('',
	(r'^export/master.zip', export.export),
	(r'^export/slave.zones', export.slave),
	(r'^export/zonelist.txt', export.zonelist),
)
