from models import *
from django.contrib.gis import admin

admin.site.register(Path, admin.OSMGeoAdmin)
