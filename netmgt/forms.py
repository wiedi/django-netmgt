from django import forms
from django.core.validators import validate_integer
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str as smart_text
from .models import Zone, ZoneRecord, TemplateRecord
import IPy


def full_domain_validator(hostname):
	import re
	"""
	http://stackoverflow.com/a/17822192
	Fully validates a domain name as compilant with the standard rules:
		- Composed of series of labels concatenated with dots, as are all domain names.
		- Each label must be between 1 and 63 characters long.
		- The entire hostname (including the delimiting dots) has a maximum of 255 characters.
		- Only characters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9'.
		- Labels can't start or end with a hyphen.
	"""
	HOSTNAME_LABEL_PATTERN = re.compile("(?!-)[A-Z0-9-]+(?<!-)$", re.IGNORECASE)
	hostname = smart_text(hostname)
	if not hostname:
		return
	if len(hostname) > 255:
		raise forms.ValidationError(_("The domain name cannot be composed of more than 255 characters."))
	if hostname[-1:] == ".":
		hostname = hostname[:-1]  # strip exactly one dot from the right, if present
	for label in hostname.split("."):
		if len(label) > 63:
			raise forms.ValidationError(
				_("The label '%(label)s' is too long (maximum is 63 characters).") % {'label': label})
		if not HOSTNAME_LABEL_PATTERN.match(label):
			raise forms.ValidationError(_("Unallowed characters in label '%(label)s'.") % {'label': label})


def ip_version_validator(value, version, message):
	try:
		ip, v = IPy.parseAddress(value)
	except ValueError:
		raise forms.ValidationError(message)
	if v != version:
		raise forms.ValidationError(message)


class ZoneAdminForm(forms.ModelForm):
	def clean_name(self):
		name = self.cleaned_data["name"].encode('idna').decode("utf-8")
		full_domain_validator(name)
		if name[-1] == '.':
			raise forms.ValidationError("Zone name can't end with '.'")
		return name

	class Meta:
		model = Zone
		exclude = []


class RecordForm(forms.ModelForm):
	def clean_value(self):
		rtype = self.cleaned_data.get("type", None)
		value = self.cleaned_data.get("value", None)
		if rtype == 'A':
			ip_version_validator(value, 4, "Need valid IPv4 Address for A record")
		elif rtype == 'AAAA':
			ip_version_validator(value, 6, "Need valid IPv6 Address for AAAA record")
		elif rtype == 'MX':
			values = value.split()
			if len(values) != 2:
				raise forms.ValidationError("Need priority and FQDN for MX record")
			prio, fqdn = values
			validate_integer(prio)
			full_domain_validator(fqdn)
		return value

class ZoneRecordForm(RecordForm):
	class Meta:
		model = ZoneRecord
		exclude = []

class TemplateRecordForm(RecordForm):
	class Meta:
		model = TemplateRecord
		exclude = []
