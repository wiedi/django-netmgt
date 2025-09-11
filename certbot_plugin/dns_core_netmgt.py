import requests
from certbot.plugins import dns_common


class Authenticator(dns_common.DNSAuthenticator):
	"""DNS Authenticator for core.io netmgt"""

	description = "Setup dns-01 challanges via core.io netmgt API."

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.credentials = None

	def more_info(self):
		return "Setup dns-01 challanges via core.io netmgt API."

	@classmethod
	def add_parser_arguments(cls, add):
		super(Authenticator, cls).add_parser_arguments(
			add, default_propagation_seconds=300
		)
		add("credentials", help="netmgt credentials INI file.")

	def _setup_credentials(self):
		self.credentials = self._configure_credentials(
			"credentials",
			"netmgt credentials INI file",
			{
				"endpoint": "URL of the netmgt API.",
				"admin_token": "admin token for th netmgt API.",
			},
		)

	def _perform(self, domain, validation_name, validation):
		self._netmgt_post(domain, {"acme_challange": validation})

	def _cleanup(self, domain, validation_name, validation):
		self._netmgt_post(domain, {"acme_challange": ""})

	def _netmgt_post(self, domain, data):
		endpoint = self.credentials.conf("endpoint")
		admin_token = self.credentials.conf("admin_token")
		url = f"{endpoint}/netmgt/api/zone/{domain}/set_acme_challange/"
		data["acme_admin_token"] = admin_token
		req = requests.post(url, json=data)
		req.raise_for_status()
