from django.core.management.base import BaseCommand

from ...models import Sector


class Command(BaseCommand):
    help = "Rebuilds the sectors MPTT tree"

    def handle(self, *args, **options):
        self.stdout.write(f"Rebuilding tree ({Sector.objects.count()} sectors)")
        Sector.objects.rebuild()
        self.stdout.write(self.style.SUCCESS("Successfully rebuilt tree"))
