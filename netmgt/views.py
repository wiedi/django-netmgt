from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from netmgt.serializers import *

class TemplateViewSet(viewsets.ModelViewSet):
	queryset = Template.objects.all()
	serializer_class = TemplateSerializer
	permission_classes = [IsAuthenticated]
	lookup_value_regex = '[0-9a-zA-Z._ -]+'

class ZoneViewSet(viewsets.ModelViewSet):
	queryset = Zone.objects.all()
	serializer_class = ZoneSerializer
	permission_classes = [IsAuthenticated]
	lookup_value_regex = '[0-9a-zA-Z.]+'

class TemplateRecordViewSet(viewsets.ModelViewSet):
	queryset = TemplateRecord.objects.all()
	serializer_class = TemplateRecordSerializer
	permission_classes = [IsAuthenticated]

class ZoneRecordViewSet(viewsets.ModelViewSet):
	queryset = ZoneRecord.objects.all()
	serializer_class = ZoneRecordSerializer
	permission_classes = [IsAuthenticated]

class OperatingSystemViewSet(viewsets.ModelViewSet):
	queryset = OperatingSystem.objects.all()
	serializer_class = OperatingSystemSerializer
	permission_classes = [IsAuthenticated]
	lookup_value_regex = '[0-9a-zA-Z._ -]+'

class DeviceTypeViewSet(viewsets.ModelViewSet):
	queryset = DeviceType.objects.all()
	serializer_class = DeviceTypeSerializer
	permission_classes = [IsAuthenticated]
	lookup_value_regex = '[0-9a-zA-Z._ -]+'

class ContactViewSet(viewsets.ModelViewSet):
	queryset = Contact.objects.all()
	serializer_class = ContactSerializer
	permission_classes = [IsAuthenticated]

class DeviceViewSet(viewsets.ModelViewSet):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer
	permission_classes = [IsAuthenticated]

class AddressViewSet(viewsets.ModelViewSet):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer
	permission_classes = [IsAuthenticated]

