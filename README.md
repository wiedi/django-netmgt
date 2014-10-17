# Django Network Management Tool

Webinterface to manage DNS Configuration for Bind and NSD.

## Configuration

in the `settings.py` you might want to adjust:

```
NETMGT_DEFAULT_TTL = 3600
NETMGT_DEFAULT_NAMESERVERS = [
	'ns1.example.com',
	'ns2.example.com',
	'ns3.example.com',
]
NETMGT_HOSTMASTER = 'hostmaster.example.com'
NETMGT_SOA = {
	'refresh': '2d',
	'retry':   '15M',
	'expiry':  '2w',
	'minimum': '1h',
}
````
