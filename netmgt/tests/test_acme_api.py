import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from netmgt.models import Zone
from netmgt.tests.factories import ZoneFactory


@pytest.mark.django_db
def test_update_acme_challange():
	zone = ZoneFactory()
	assert zone.acme_admin_token
	assert not zone.acme_challange

	url = reverse("zone-set-acme-challange", args=[zone.name])
	client = APIClient()

	response = client.post(
		url, {"acme_admin_token": zone.acme_admin_token, "acme_challange": "random"}
	)

	assert response.status_code == status.HTTP_200_OK, response.json()
	zone.refresh_from_db()

	assert zone.acme_admin_token
	assert zone.acme_challange == "random"


@pytest.mark.django_db
def test_update_acme_challange_empty_token():
	zone = ZoneFactory(acme_challange="ok")
	Zone.objects.update(acme_admin_token="")
	zone.refresh_from_db()
	assert not zone.acme_admin_token
	assert zone.acme_challange

	url = reverse("zone-set-acme-challange", args=[zone.name])
	client = APIClient()

	response = client.post(url, {"acme_admin_token": "", "acme_challange": "random"})

	assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()
	zone.refresh_from_db()

	assert not zone.acme_admin_token
	assert zone.acme_challange == "ok"


@pytest.mark.django_db
def test_update_acme_challange_unset():
	zone = ZoneFactory(acme_challange="ok")
	assert zone.acme_admin_token
	assert zone.acme_challange

	url = reverse("zone-set-acme-challange", args=[zone.name])
	client = APIClient()

	response = client.post(
		url,
		{
			"acme_admin_token": zone.acme_admin_token,
		},
	)

	assert response.status_code == status.HTTP_200_OK, response.json()
	zone.refresh_from_db()

	assert zone.acme_admin_token
	assert not zone.acme_challange
