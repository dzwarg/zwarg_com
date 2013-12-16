from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.utils.timezone import utc
from django.contrib.auth.models import User

from csv import DictReader
from datetime import timedelta, datetime as dt

from mezzanine.utils.sites import current_site_id
from mezzanine.blog.models import BlogCategory, BlogPost

def parse_datetime(strtime):
    """
    Parse a string date, time & tz into a datetime object:

    2003-03-20 05:00:00-07

    """
    offset = int(strtime[-3:])
    date_time = dt.strptime(strtime[:-4], '%Y-%m-%d %H:%M:%S')

    offset = timedelta(hours=offset)
    return (date_time + offset).replace(tzinfo=utc)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--truncate',
            action='store_true',
            dest='truncate',
            default=False,
            help='Truncate all entries before importing'),
        )

    def handle(self, *args, **options):
        if options['truncate']:
            print 'Deleting Blog Entries:'
            for entry in BlogPost.objects.all():
                print '\t{}'.format(entry.title)
            BlogPost.objects.all().delete()

        category_lookup = {}

        with open('db_export/blog_category.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                category_lookup[row['id']] = BlogCategory.objects.get(title=row['name']).id

        site_id = current_site_id()
        user = User.objects.get(id=1)
        publish_lookup = {'t': 2, 'f': 1}

        with open('db_export/blog_entry.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                post = BlogPost.objects.create(
                    user=user,
                    site_id=site_id, 
                    title=row['title'],
                    slug=slugify(unicode(row['slug'])),
                    allow_comments=False,
                    content=row['body'],
                    in_sitemap=False,
                    status=publish_lookup[row['published']],
                    publish_date=parse_datetime(row['pub_date'])
                )
                post.categories=[category_lookup[row['category_id']]]
                post.save()


