from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from netmgt.serializers import *


class TemplateViewSet(viewsets.ModelViewSet):
	queryset = Template.objects.all()
	serializer_class = TemplateSerializer
	permission_classes = [IsAuthenticated]
	lookup_value_regex = "[0-9a-zA-Z._ -]+"


class ZoneViewSet(viewsets.ModelViewSet):
	queryset = Zone.objects.all()
	serializer_class = ZoneSerializer
	permission_classes = [IsAuthenticated]
	lookup_value_regex = "[0-9a-zA-Z.-]+"

	@action(detail=True, methods=["post"], permission_classes=[])
	def set_acme_challange(self, request, pk):
		zone = self.get_object()
		serializer = SetACMEChallangeSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if (
			not zone.acme_admin_token
			or serializer.validated_data.get("acme_admin_token")
			!= zone.acme_admin_token
		):
			raise AuthenticationFailed()
		zone.acme_challange = serializer.validated_data.get("acme_challange", "")
		zone.save()
		return Response(SetACMEChallangeSerializer(zone).data)


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
	lookup_value_regex = "[0-9a-zA-Z._ -]+"


class DeviceTypeViewSet(viewsets.ModelViewSet):
	queryset = DeviceType.objects.all()
	serializer_class = DeviceTypeSerializer
	permission_classes = [IsAuthenticated]
	lookup_value_regex = "[0-9a-zA-Z._ -]+"


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
