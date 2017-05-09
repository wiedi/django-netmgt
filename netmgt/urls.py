from django.conf.urls import url
from .export import *

urlpatterns = [
	url(r'^export/zones.zip', export),
	url(r'^export/zones.txt', text),
]
