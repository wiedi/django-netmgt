from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from netmgt.models import CachedZone, Zone, Address

class Command(BaseCommand):
	help = 'Clean Zone cache from stale zones'

	def add_arguments(self, parser):
		parser.add_argument('--force', action = 'store_true', dest = 'force', default = False, help = 'Drop complete cache')


	def handle(self, *args, **options):
		qs = CachedZone.objects.all()

		if not options['force']:
			fwd = Zone.objects.all().extra(select={'name_with_dot': '`name` || "."'},).values_list('name_with_dot', flat=True)
			rev = Address.objects.values_list('reverse_zone', flat=True).distinct()
			qs = CachedZone.objects.exclude(key__in=fwd).exclude(key__in=rev)

		qs.delete()
