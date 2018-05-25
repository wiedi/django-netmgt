from django.db import models
import IPy

default_length = 250

class Template(models.Model):
	name = models.CharField(max_length=default_length, primary_key=True, unique=True)

	def __unicode__(self):
		return self.name


class Zone(models.Model):
	name      = models.CharField(max_length=default_length, primary_key=True, unique=True)
	ttl       = models.IntegerField(null=True, blank=True, verbose_name='TTL')
	templates = models.ManyToManyField(Template, blank=True)

	def __unicode__(self):
		return self.name + '.'


class Record(models.Model):
	RECORD_TYPES = (
		('A',      'A'),
		('AAAA',   'AAAA'),
		('CERT',   'CERT'),
		('CNAME',  'CNAME'),
		('DNSKEY', 'DNSKEY'),
		('DS',     'DS'),
		('DNSKEY', 'DNSKEY'),
		('KEY',    'KEY'),
		('LOC',    'LOC'),
		('MX',     'MX'),
		('NAPTR',  'NAPTR'),
		('NS',     'NS'),
		('NSEC',   'NSEC'),
		('PTR',    'PTR'),
		('RRSIG',  'RRSIG'),
		('SPF',    'SPF'),
		('SRV',    'SRV'),
		('TXT',    'TXT'),
	)

	name  = models.CharField(max_length=default_length, blank=True)
	ttl   = models.IntegerField(null=True, blank=True, verbose_name='TTL')
	type  = models.CharField(max_length=8, choices=RECORD_TYPES)
	value = models.CharField(max_length=default_length)

	class Meta:
		abstract = True

	def format(self, zone):
		v = self.value
		if self.type in ('TXT', 'SPF'):
			v = '"' + v + '"'
		ttl = (' ' + str(self.ttl)) if self.ttl else ''
		return (self.name + '.' if self.name else '') + zone + ttl + ' IN ' + self.type + ' ' + v

	def __unicode__(self):
		return self.format('')


class ZoneRecord(Record):
	zone = models.ForeignKey(Zone)

	def __unicode__(self):
		return self.format(str(self.zone))


class TemplateRecord(Record):
	template  = models.ForeignKey(Template)


class OperatingSystem(models.Model):
	name = models.CharField(max_length=default_length, primary_key=True, unique=True)

	def __unicode__(self):
		return self.name

class DeviceType(models.Model):
	name = models.CharField(max_length=default_length, primary_key=True, unique=True)

	def __unicode__(self):
		return self.name

class Contact(models.Model):
	nick  = models.CharField(max_length=default_length, primary_key=True, unique=True)
	name  = models.CharField(max_length=default_length)
	email = models.EmailField()

	def __unicode__(self):
		return self.nick

class Device(models.Model):
	name    = models.CharField(max_length=default_length)
	contact = models.ForeignKey(Contact)
	type    = models.ForeignKey(DeviceType)
	os      = models.ForeignKey(OperatingSystem, verbose_name='Operating System')
	info    = models.CharField(max_length=default_length, blank=True)

	def __unicode__(self):
		return self.name


class Address(models.Model):
	device       = models.ForeignKey(Device)
	ip           = models.GenericIPAddressField()
	prefix_len   = models.IntegerField(verbose_name='Prefix Length')
	name         = models.CharField(max_length=default_length)
	zone         = models.ForeignKey(Zone)
	reverse_zone = models.CharField(max_length=default_length)

	def save(self, *args, **kwargs):
		a = IPy.IP(self.ip)
		prefix_len = self.prefix_len
		if a.version() == 4 and self.prefix_len < 24:
			# RFC 2317 is an ugly hack which only works for sub-/24 e.g. not
			# for /23. Do not use it. Let's fix it to 24
			prefix_len = 24

		self.reverse_zone = IPy.IP(self.ip).make_net(prefix_len).reverseName()
		super(Address, self).save(*args, **kwargs)

	def subnet(self):
		"Returns the Subnet"
		return str(IPy.IP(self.ip).make_net(self.prefix_len))

	def __unicode__(self):
		return self.ip + '/' + str(self.prefix_len)


class CachedZone(models.Model):
	key     = models.CharField(max_length=default_length, primary_key=True, unique=True)
	tag     = models.CharField(max_length=default_length)
	value   = models.TextField(max_length=default_length)
	updated = models.DateTimeField()

	def __unicode__(self):
		return self.updated.strftime('%s') + ': ' + self.key
