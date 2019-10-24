from rest_framework import serializers
from netmgt.models import *

class TemplateRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = TemplateRecord
		fields = ['id', 'template', 'name', 'ttl', 'type', 'value']

class ZoneRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = ZoneRecord
		fields = ['id', 'zone', 'name', 'ttl', 'type', 'value']


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['id', 'device', 'ip', 'prefix_len', 'name', 'zone', 'reverse_zone']
		read_only_fields = ['reverse_zone']

class DeviceSerializer(serializers.ModelSerializer):
	addresses = AddressSerializer(many=True, read_only=True)

	class Meta:
		model = Device
		fields = ['id', 'name', 'contact', 'type', 'os', 'info', 'addresses']


class TemplateSerializer(serializers.ModelSerializer):
	records = TemplateRecordSerializer(many=True, read_only=True)

	class Meta:
		model = Template
		fields = ['name', 'records']

class ZoneSerializer(serializers.ModelSerializer):
	records   = ZoneRecordSerializer(many=True, read_only=True)
	addresses = AddressSerializer(many=True, read_only=True)

	class Meta:
		model = Zone
		fields = ['name', 'ttl', 'templates', 'records', 'addresses']


class OperatingSystemSerializer(serializers.ModelSerializer):
	class Meta:
		model = OperatingSystem
		fields = ['name']

class DeviceTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = DeviceType
		fields = ['name']

class ContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contact
		fields = ['nick', 'name', 'email']
