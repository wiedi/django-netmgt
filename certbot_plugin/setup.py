from setuptools import setup

setup(
	name="certbot-netmgt",
	version="26.5.28",
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
