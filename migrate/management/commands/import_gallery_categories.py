from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.db.models import Q

from csv import DictReader

from mezzanine.utils.sites import current_site_id
from mezzanine.galleries.models import Gallery

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--truncate',
            action='store_true',
            dest='truncate',
            default=False,
            help='Truncate all gallery categories before importing'),
        )

    def handle(self, *args, **options):
        if options['truncate']:
            print 'Deleting Gallery Categories:'
            for gallery in Gallery.objects.filter(~Q(title='Gallery')):
                print '\t{}'.format(gallery.title)
            Gallery.objects.filter(~Q(title='Gallery')).delete()

        site_id = current_site_id()
        child_galleries = []

        parent_lookup = {
            '': Gallery.objects.get(title='Gallery').id
        }

        publish_lookup = {'t': 2, 'f': 1}

        with open('db_export/gallery_category.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                options = {
                    'site_id':site_id,
                    'title':row['name'],
                    'content':row['description'],
                    'in_sitemap':True,
                    'in_menus': '',
                    'status':publish_lookup[row['published']]
                }
                if row['parent_id'] in parent_lookup:
                    options['parent_id'] = parent_lookup[row['parent_id']]
                else:
                    options['parent_id'] = row['parent_id']
                    child_galleries.append(options)
                    continue

                print 'Creating Gallery {}'.format(row['name'])

                g = Gallery.objects.create(**options)
                parent_lookup[row['id']] = g.id

        # recursively add new galleries to parents that didn't exist in N-1 pass
        while len(child_galleries) > 0:
            orphaned = []
            for child in child_galleries:
                if child['parent_id'] in parent_lookup:
                    row_id = child['parent_id']
                    child['parent_id'] = Gallery.objects.get(id=parent_lookup[row_id]).id

                    print 'Creating Gallery {}'.format(child['title'])
                    g = Gallery.objects.create(**child)
                    parent_lookup[row_id] = g.id
                else:
                    orphaned.append(child)

            child_galleries = orphaned