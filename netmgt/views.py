from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from netmgt.models import ZoneRecord
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

	@extend_schema(
		request=SetACMEChallangeSerializer,
		responses=ResonseACMEChallangeSerializer,
	)
	@action(
		detail=True,
		methods=["post"],
		permission_classes=[],
		url_path=r"set_acme_challange/(?P<domain>[a-zA-Z0-9.*-]+)",
	)
	def set_acme_challange(self, request, pk, domain):
		zone = self.get_object()
		serializer = SetACMEChallangeSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if (
			not zone.acme_admin_token
			or serializer.validated_data.get("acme_admin_token")
			!= zone.acme_admin_token
		):
			raise AuthenticationFailed()

		is_wildcard = domain.startswith("*.")
		effective_domain = domain[2:] if is_wildcard else domain

		acme_value = serializer.validated_data.get("acme_challange", "")

		if effective_domain == zone.name:
			zone.acme_challange = acme_value
			zone.save()
		else:
			subdomain_prefix = effective_domain[: -(len(zone.name) + 1)]
			record_name = f"_acme-challenge.{subdomain_prefix}"
			ZoneRecord.objects.filter(zone=zone, name=record_name, type="TXT").delete()
			if acme_value:
				ZoneRecord.objects.create(
					zone=zone, name=record_name, type="TXT", value=acme_value
				)

		return Response(ResonseACMEChallangeSerializer({"domain": domain, "acme_challange": acme_value}).data)


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
