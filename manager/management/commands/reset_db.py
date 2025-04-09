from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Flush DB and load initial dump"

    def handle(self, *args, **kwargs):
        self.stdout.write("Resetting DB...")
        call_command("flush", "--no-input")
        call_command("migrate")
        call_command("loaddata", "dump.json")
        self.stdout.write(self.style.SUCCESS("Done!"))