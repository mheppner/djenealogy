from djenealogy.models import *
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from djenealogy.importer import GedcomParser


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        
    )
    
    args = '<gedcom_id gedcom_id ...'
    help = 'Parse the file attached to a Gedcom object'

    def handle(self, *args, **options):
        self.options = options
        self.options['verbosity'] = int(self.options['verbosity'])
        
        if len(args) == 0:
            self.stderr.write('You must supply a gedcom slug')
            gedcoms = [x.slug for x in Gedcom.objects.all()]
            self.stdout.write('IDs: %s' % gedcoms)
            
        else:
            for gedcom_slug in args:
                try:
                    g = Gedcom.objects.get(slug=gedcom_slug)
                except Gedcom.DoesNotExist:
                    raise CommandError('Gedcom %s does not exist' % gedcom_slug)
                else:
                    GedcomParser(g).parse()
            
            