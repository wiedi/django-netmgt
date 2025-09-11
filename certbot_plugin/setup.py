from setuptools import setup

setup(
	name="certbot-netmgt",
	version="25.9.11",
	description="Certbot plugin for django-netmgt",
	package="dns_core_netmgt.py",
	install_requires=[
		"certbot",
	],
	entry_points={
		"certbot.plugins": [
			"dns-netmgt = dns_core_netmgt:Authenticator",
		],
	},
)
