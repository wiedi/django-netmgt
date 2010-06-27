from setuptools import setup, find_packages
setup(
	name = "django-netmgt",
	version = "0.1",
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	install_requires = ['IPy'],
	author = "Sebastian Wiedenroth",
	author_email = "wiedi@frubar.net",
	description = "network management tool for django",
	license = "BSD",
)

