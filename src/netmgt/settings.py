NETMGT_SITE_NAME = 'example'

NETMGT_DEFAULT_TTL = 86400

NETMGT_SOA = {
	'refresh': '2d',
	'retry': '15M',
	'expiry': '2w',
	'minimum': '1h',
}

NETMGT_DEFAULT_NAMESERVERS = [
	'ns1.example.com.',
	'ns2.example.com.',
	'ns3.example.com.',
]

NETMGT_MASTERS = [
	'203.0.113.1',
	'203.0.113.2',
]

NETMGT_HOSTMASTER = 'hostmaster.example.com'
