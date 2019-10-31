from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = """
        Load infrastructure projects from a csv file. The following headers are expected:
            Function,
            Project Decription,
            Project Number,
            Type,
            MTSF Service Outcome,
            IUDF,
            Own Strategic Objectives,
            Asset Class,
            Asset Sub-Class,
            Ward Location,
            GPS Longitude,
            GPS Latitude
    """

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
