from django.contrib.gis.db import models

import manager

from mezzanine.core.models import RichText
from mezzanine.pages.models import Page

class Path(Page, RichText):
    #geom = models.MultiLineStringField()
    #objects = manager.DisplayableGeoManager()

    class Meta:
        verbose_name = "Path"
        verbose_name_plural = "Paths"
