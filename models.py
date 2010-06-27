from django.db import models
import IPy

default_length = 250

class Zone(models.Model):
	name = models.CharField(max_length=default_length, primary_key=True)
	ttl  = models.IntegerField(null=True, blank=True, verbose_name='TTL')
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
	);

	zone  = models.ForeignKey(Zone)
	name  = models.CharField(max_length=default_length, blank=True)
	ttl   = models.IntegerField(null=True, blank=True, verbose_name='TTL')
	type  = models.CharField(max_length=8, choices=RECORD_TYPES)
	value = models.CharField(max_length=default_length)

	def __unicode__(self):
		v = self.value
		if self.type in ('TXT', 'SPF'):
			v = '"' + v + '"'
		ttl = (' ' + str(self.ttl)) if self.ttl else ''
		return (self.name + '.' if self.name else '') + unicode(self.zone) + ttl + ' IN ' + self.type + ' ' + v


class OperatingSystem(models.Model):
	name = models.CharField(max_length=default_length)

	def __unicode__(self):
		return self.name

class DeviceType(models.Model):
	name = models.CharField(max_length=default_length)

	def __unicode__(self):
		return self.name

class Contact(models.Model):
	nick  = models.CharField(max_length=default_length)
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
	device     = models.ForeignKey(Device)
	ip         = models.IP6AddressField()
	prefix_len = models.IntegerField(verbose_name='Prefix Length')
	name       = models.CharField(max_length=default_length)
	zone       = models.ForeignKey(Zone)
	
	def subnet(self):
		"Returns the Subnet"
		return str(IPy.IP(self.ip).make_net(self.prefix_len))

	def __unicode__(self):
		return self.ip + '/' + str(self.prefix_len)

