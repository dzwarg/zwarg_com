from django.contrib.gis.db import models

class Path(models.Model):
    geom = models.MultiLineStringField()
    objects = models.GeoManager()