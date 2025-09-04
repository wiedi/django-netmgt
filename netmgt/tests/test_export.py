import pytest
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse

from netmgt.export import generate_bind_conf, generate_zones
from netmgt.models import CachedZone
from netmgt.tests.factories import (
	AddressFactory,
	UserFactory,
	ZoneFactory,
	ZoneRecordFactory,
)


@pytest.mark.django_db
def test_export_text(client):
	cache.clear()
	AddressFactory()

	url = reverse("export_text")

	# generate cached zone
	response = client.get(url, {"token": settings.NETMGT_DNS_TOKEN})

	cached = CachedZone.objects.first()
	serial = cached.updated.strftime("%s")

	response = client.get(url, {"token": settings.NETMGT_DNS_TOKEN})
	assert response.status_code == 200
	assert response.content.decode("utf-8").splitlines() == [
		"; zone: zone-0.example.com.",
		"$TTL    3600",
		f"@                  IN      SOA     ns1.example.com. hostmaster.example.com. ( {serial} 2d 15M 2w 1h )",
		"        86400      IN      NS      ns1.example.com.",
		"        86400      IN      NS      ns2.example.com.",
		"        86400      IN      NS      ns3.example.com.",
		"; devices",
		"addr-0.zone-0.example.com. IN AAAA 2001:db8::",
		"; records",
		"",
		"",
		"; zone: 0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
		"$TTL    3600",
		f"@                  IN      SOA     ns1.example.com. hostmaster.example.com. ( {serial} 2d 15M 2w 1h )",
		"        86400      IN      NS      ns1.example.com.",
		"        86400      IN      NS      ns2.example.com.",
		"        86400      IN      NS      ns3.example.com.",
		"; devices",
		"0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. IN PTR addr-0.zone-0.example.com.",
	]


@pytest.mark.django_db
def test_export_text_query_count(client, django_assert_max_num_queries):
	cache.clear()
	for i in range(10):
		z = ZoneFactory(name=f"test{i}.example.com")
		ZoneRecordFactory.create_batch(20, zone=z)
		AddressFactory.create_batch(20, zone=z)

	url = reverse("export_text")

	# Still too high
	with django_assert_max_num_queries(53):
		response = client.get(url, {"token": settings.NETMGT_DNS_TOKEN})
	assert response.status_code == 200


@pytest.mark.django_db
def test_generate_bind_conf():
	address = AddressFactory()
	zones = generate_zones()
	out = generate_bind_conf(zones)
	assert out.splitlines() == [
		"# generated - do not modify",
		f'zone "{address.zone.name}." {{ type master; file "zones/core/{address.zone.name}.zone"; }};',
		'zone "0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa." { type master; file "zones/core/0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.zone"; };',
	]
