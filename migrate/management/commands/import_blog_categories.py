from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from csv import DictReader

from mezzanine.utils.sites import current_site_id
from mezzanine.blog.models import BlogCategory

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--truncate',
            action='store_true',
            dest='truncate',
            default=False,
            help='Truncate all categories before importing'),
        )

    def handle(self, *args, **options):
        if options['truncate']:
            print 'Deleting Blog Categories:'
            for category in BlogCategory.objects.all():
                print '\t{}'.format(category.title)
            BlogCategory.objects.all().delete()

        site_id = current_site_id()
        new_categories = [];

        with open('db_export/blog_category.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                new_categories.append(
                    BlogCategory(site_id=site_id, title=row['name'],slug=row['name'])
                )

        BlogCategory.objects.bulk_create(new_categories)

