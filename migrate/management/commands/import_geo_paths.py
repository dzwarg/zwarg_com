from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry

import sys
import csv

from csv import DictReader

from mezzanine.utils.sites import current_site_id
from mezzanine.blog.models import BlogPost

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--truncate',
            action='store_true',
            dest='truncate',
            default=False,
            help='Truncate all geometries before importing'),
        )

    def handle(self, *args, **options):
        csv.field_size_limit(sys.maxsize)

        if options['truncate']:
            print 'Deleting BlogPost Geo:'
            for post in BlogPost.objects.filter(geom__isnull=False):
                print '\t{}'.format(post.title)
            BlogPost.objects.filter(geom__isnull=False).update(geom=None)

        entry_lookup = {}

        with open('db_export/blog_entry.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                entry_lookup[row['id']] = BlogPost.objects.filter(title=row['title']).first().id

        path_lookup = {}

        with open('db_export/zwarg_entrygeo.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                path_lookup[row['path_id']] = entry_lookup[row['entry_id']]

        site_id = current_site_id()
        user = User.objects.get(id=1)
        publish_lookup = {'t': 2, 'f': 1}

        import ipdb; ipdb.set_trace()

        with open('db_export/geo_path.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                geom = GEOSGeometry(row['geom'])
                if geom.geom_type == 'MultiLineString':
                    geom = geom[0]

                post = BlogPost.objects.get(id=path_lookup[row['id']])
                post.geom = geom
                post.save()


