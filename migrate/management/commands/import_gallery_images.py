from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from cStringIO import StringIO
from PIL import Image
from urllib2 import urlopen
from csv import DictReader
import os, sys

from mezzanine.utils.sites import current_site_id
from mezzanine.galleries.models import Gallery, GalleryImage

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--truncate',
            action='store_true',
            dest='truncate',
            default=False,
            help='Truncate all gallery images before importing'),
        )

    def handle(self, *args, **options):
        if options['truncate']:
            print 'Deleting Gallery Images:'
            for image in GalleryImage.objects.all():
                print '\t{}'.format(image.file)
            GalleryImage.objects.all().delete()

        gallery_lookup = {}

        with open('db_export/gallery_category.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                print row['name']
                gallery_lookup[row['id']] = Gallery.objects.get(title=row['name'])

        site_id = current_site_id()

        progress = 80
        count = 0

        with open('db_export/gallery_photo.csv', 'rb') as f:
            reader = DictReader(f)
            for row in reader:
                url = 'http://www.zwarg.com/media/gallery/images/{category_id}/{filename}'.format(
                    category_id=row['category_id'],
                    filename=row['media']
                )
                gallery = gallery_lookup[row['category_id']]

                webio = urlopen(url)
                data = webio.read()
                webio.close()

                try:
                    image = Image.open(StringIO(data))
                    image.load()
                    image = Image.open(StringIO(data))
                    image.verify()
                except:
                    print '\nImage "{}" could not be verified, skipping.\n'.format(url)
                    continue

                name = os.path.split(url)[1]
                path = os.path.join('uploads', 'galleries', gallery.slug, name)

                
                saved_path = default_storage.save(path, ContentFile(data))

                GalleryImage.objects.create(gallery=gallery, file=saved_path, description=row['description'])

                sys.stdout.write('.')
                sys.stdout.flush()

                if count > 0 and count % progress == 0:
                    sys.stdout.write(' | {}\n'.format(count))
                    sys.stdout.flush()
