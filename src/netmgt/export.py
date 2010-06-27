from django.http import HttpResponse
import zipfile
import tempfile
import IPy
import time
from models import Zone, Record, Address, Device
from django.conf import settings

def create_soa(ttl = None):
	if not ttl:
		ttl = settings.NETMGT_DEFAULT_TTL
		
	soa = '$TTL    ' + str(ttl) + '\n'
	soa +='@       IN      SOA     ' + settings.NETMGT_MASTERS[0] + ' ' + settings.NETMGT_HOSTMASTER + \
		' ( {serial} {refresh} {retry} {expiry} {minimum} )'.format(serial=int(time.time()), **SOA)
	for ns in settings.NETMGT_DEFAULT_NAMESERVERS:
		soa += "        IN      NS      " + ns + "\n"
	return soa
	
def export(request):
	response = HttpResponse(mimetype='application/x-zip')
	response['Content-Disposition'] = 'attachment; filename=master.zip'

	files = {}

	for zone in Zone.objects.all():
		zn = unicode(zone)

		files['fwd/' + zn] = create_soa(zone.ttl)
		for record in zone.record_set.all():
			files['fwd/' + zn] += unicode(record) + "\n"

		for address in zone.address_set.all():
			a = IPy.IP(address.ip)
			rz = a.make_net(address.prefix_len).reverseName()
			if 'rev/' + rz not in files:
				files['rev/' + rz] = create_soa()

			type = 'A' if a.version() == 4 else 'AAAA'

			files['fwd/' + zn] += address.name + '.' + zn + ' IN ' + type + ' ' + address.ip + '\n'
			if address.prefix_len > 24 and address.prefix_len < 32:
				files['rev/' + rz] += a.reverseName().split('.')[0] + '.' + rz + ' IN PTR ' + address.name + '.' + zn + '\n'
			else:
				files['rev/' + rz] += a.reverseName() + ' IN PTR ' + address.name + '.' + zn + '\n'

	z = zipfile.ZipFile(response, mode='w')
	fruky_zones = "# generated - don't touch\n"
	for k in files:
		z.writestr(settings.NETMGT_SITE_NAME + '/' + k + 'zone', files[k])
		fruky_zones += 'zone "' + k[4:] + '" { type master; file "pri/' + settings.NETMGT_SITE_NAME + '/' + k + 'zone"; };\n'
	z.writestr(settings.NETMGT_SITE_NAME + '.zones', fruky_zones)

	return response
	

def slave(request):
	response = HttpResponse(mimetype='text/plain')
	masters = '; '.join(settings.NETMGT_MASTERS) + ';'
	tpl = 'zone "%s" {type slave; masters { ' + masters + ' }; file "sec/' + settings.NETMGT_SITE_NAME + '/%s/%szone"; };\n'

	done = []

	for zone in Zone.objects.all():
		zn = unicode(zone)
		response.write(tpl % (zn[:-1], 'fwd', zn))
		for address in zone.address_set.all():
			rz = IPy.IP(address.ip).make_net(address.prefix_len).reverseName()
			if rz not in done:
				done += [rz]
				response.write(tpl % (rz[:-1], 'rev', rz))
	return response

def zonelist(request):
	response = HttpResponse(mimetype='text/plain')

	for zone in Zone.objects.all():
		response.write(unicode(zone)[:-1] + "\n")

	return response

