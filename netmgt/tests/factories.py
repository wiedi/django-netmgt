import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

from netmgt.models import Zone, Template, ZoneRecord, TemplateRecord, DeviceType, Contact, OperatingSystem, Device, Address

class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    class Meta:
        model = User

class ZoneFactory(DjangoModelFactory):
	name = factory.Sequence(lambda n: f"zone-{n}.example.com")

	class Meta:
		model = Zone

class TemplateFactory(DjangoModelFactory):
	name = factory.Sequence(lambda n: f"Template-{n}")

	class Meta:
		model = Template

class ZoneRecordFactory(DjangoModelFactory):
	zone = factory.SubFactory(ZoneFactory)
	name = factory.Sequence(lambda n: f"record-{n}")
	type = "A"
	value = "127.0.0.1"

	class Meta:
		model = ZoneRecord

class TemplateRecordFactory(DjangoModelFactory):
	template = factory.SubFactory(TemplateFactory)
	name = factory.Sequence(lambda n: f"record-{n}")
	type = "A"
	value = "127.0.0.1"

	class Meta:
		model = TemplateRecord

class DeviceTypeFactory(DjangoModelFactory):
	name = factory.Sequence(lambda n: f"DeviceType{n}")

	class Meta:
		model = DeviceType

class OperatingSystemFactory(DjangoModelFactory):
	name = factory.Sequence(lambda n: f"OperatingSystem{n}")

	class Meta:
		model = OperatingSystem

class ContactFactory(DjangoModelFactory):
	nick = factory.Sequence(lambda n: f"Contact{n}")
	name = factory.Sequence(lambda n: f"Contact{n}")
	email = factory.Sequence(lambda n: f"contact{n}@example.com")

	class Meta:
		model = Contact

class DeviceFactory(DjangoModelFactory):
	name = factory.Sequence(lambda n: f"device-{n}")
	contact = factory.SubFactory(ContactFactory)
	type = factory.SubFactory(DeviceTypeFactory)
	os = factory.SubFactory(OperatingSystemFactory)

	class Meta:
		model = Device

class AddressFactory(DjangoModelFactory):
	device = factory.SubFactory(DeviceFactory)
	zone = factory.SubFactory(ZoneFactory)
	name = factory.Sequence(lambda n: f"addr-{n}")
	ip = factory.Sequence(lambda n: f"2001:db8::{n}")
	prefix_len = 64

	class Meta:
		model = Address
