SITE_NAME = 'example'

DEFAULT_TTL = 86400

SOA = {
	'refresh': '2d',
	'retry': '15M',
	'expiry': '2w',
	'minimum': '1h',
}

DEFAULT_NAMESERVERS = [
	'ns1.example.com.',
	'ns2.example.com.',
	'ns3.example.com.',
]

MASTERS = [
	'203.0.113.1',
	'203.0.113.2',
]

HOSTMASTER = 'hostmaster.example.com'

