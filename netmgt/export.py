from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import condition
from django.conf import settings
from models import *
import datetime
import hashlib
import zipfile
import IPy

def create_soa(zone, ttl = None, serial = 0):
	if not ttl:
		ttl = settings.NETMGT_DEFAULT_TTL

	soa  = '; zone: ' + zone + '\n'
	soa += '$TTL    ' + str(ttl) + '\n'
	soa += '@       IN      SOA     ' + settings.NETMGT_DEFAULT_NAMESERVERS[0] + '. ' + settings.NETMGT_HOSTMASTER + \
		'. ( {serial} {refresh} {retry} {expiry} {minimum} )\n'.format(serial=serial, **settings.NETMGT_SOA)
	for ns in settings.NETMGT_DEFAULT_NAMESERVERS:
		soa += "        IN      NS      " + ns + ".\n"
	return soa

def generate_zone(zone, serial = 0):
	out = create_soa(str(zone), zone.ttl, serial)
	out += '; devices\n'
	for address in zone.address_set.all().order_by('name', 'prefix_len'):
		record_type = 'A' if IPy.IP(address.ip).version() == 4 else 'AAAA'
		out += address.name + '.' + unicode(zone) + ' IN ' + record_type + ' ' + address.ip + '\n'

	for template in zone.templates.all().order_by('name'):
		out += '; template: ' + str(template) + '\n'
		for record in template.templaterecord_set.all().order_by('name', 'type', 'value'):
			out += record.format(str(zone)) + "\n"

	out += '; records\n'
	for record in zone.zonerecord_set.all().order_by('name', 'type', 'value'):
		out += unicode(record) + "\n"
	return out

def generate_reverse_zone(reverse_zone, serial = 0):
	out = create_soa(str(reverse_zone), None, serial)
	out += '; devices\n'
	for address in Address.objects.filter(reverse_zone = reverse_zone).order_by('ip'):
		a = IPy.IP(address.ip)
		if address.prefix_len > 24 and address.prefix_len < 32 and a.version() == 4:
			out += a.reverseName().split('.')[0] + '.' + reverse_zone + ' IN PTR ' + address.name + '.' + str(address.zone) + '\n'
		else:
			out += a.reverseName() + ' IN PTR ' + address.name + '.' + str(address.zone) + '\n'
	return out


def get_cached_zone(zone, generate_function):
	tag = hashlib.sha224(generate_function(zone)).hexdigest()
	now = datetime.datetime.now()
	defaults = {
		'tag':     tag,
		'value':   generate_function(zone, now.strftime('%s')),
		'updated': now,
	}
	cache, created = CachedZone.objects.get_or_create(key = str(zone), defaults = defaults)
	if cache.tag != tag:
		cache.__dict__.update(**defaults)
		cache.save()
	return cache.value


def generate_zones():
	zones = {}
	for zone in Zone.objects.all():
		zones[str(zone)] = get_cached_zone(zone, generate_zone)

	for reverse_zone in Address.objects.values_list('reverse_zone', flat=True).distinct():
		zones[str(reverse_zone)] = get_cached_zone(reverse_zone, generate_reverse_zone)

	return zones


def generate_bind_conf(zones):
	out = '# generated - do not modify\n'
	for zone in zones.keys():
		out += 'zone "' + zone + '" { type master; file "zones/' + zone + 'zone"; };\n'
	return out


def generate_nsd_conf(zones):
	out = '# generated - do not modify\n'
	for zone in zones.keys():
		out += 'zone:\n'
		out += '\tname: ' + zone + '\n'
		out += '\tzonefile: zones/' + zone + 'zone\n\n'
	return out


def total_last_modified(request=None):
	# refresh caches:
	generate_zones()
	try:
		return CachedZone.objects.values_list('updated', flat=True).order_by('-updated')[0]
	except IndexError:
		return datetime.datetime.now()


def etag_last_modified(request=None):
	return 'TS' + total_last_modified().strftime('%s')


def text(request):
	zones = generate_zones()
	response = HttpResponse(content_type='text/plain')
	response.write('\n\n'.join(zones.values()))
	return response


@condition(etag_func=etag_last_modified, last_modified_func=total_last_modified)
def export(request):
	zones = generate_zones()
	response = HttpResponse(content_type='application/x-zip')
	response['Content-Disposition'] = 'attachment; filename=zones.zip'
	z = zipfile.ZipFile(response, mode='w')
	for zone_name, zone in zones.items():
		filename = 'zone/' + zone_name + 'zone'
		try:
			last_modified = CachedZone.objects.values_list('updated', flat=True).get(key=zone_name)
		except ObjectDoesNotExist:
			last_modified = datetime.datetime.now()
		z.writestr(zipfile.ZipInfo(filename, date_time=last_modified.timetuple()), zone)
	last_modified = total_last_modified().timetuple()
	z.writestr(zipfile.ZipInfo('zones-bind.conf', date_time=last_modified), generate_bind_conf(zones))
	z.writestr(zipfile.ZipInfo('zones-nsd.conf',  date_time=last_modified), generate_nsd_conf(zones))
	return response