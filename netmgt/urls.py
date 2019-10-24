from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers

from netmgt.views import *
import netmgt.export as export

router = routers.DefaultRouter()
router.register(r'address',         AddressViewSet)
router.register(r'contact',         ContactViewSet)
router.register(r'device',          DeviceViewSet)
router.register(r'device_type',     DeviceTypeViewSet)
router.register(r'os',              OperatingSystemViewSet)
router.register(r'template',        TemplateViewSet)
router.register(r'template_record', TemplateRecordViewSet)
router.register(r'zone',            ZoneViewSet)
router.register(r'zone_record',     ZoneRecordViewSet)

urlpatterns = [
	path('export/zones.zip', export.export),
	path('export/zones.txt', export.text),
	url(r'^api/', include(router.urls)),
]
