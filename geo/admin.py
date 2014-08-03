from models import Path
from django.contrib.gis import admin as gis_admin
from django.contrib import admin

from copy import deepcopy
from mezzanine.core.admin import DisplayableAdmin
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import Page, RichTextPage

gis_admin.site.register(Path, gis_admin.OSMGeoAdmin)

page_fieldsets = deepcopy(PageAdmin.fieldsets)
page_fieldsets[0][1]["fields"] += ('content', 'geom',)

class GeoPageAdmin(PageAdmin):
    fieldsets = page_fieldsets

admin.site.unregister(Page)
admin.site.register(Page, GeoPageAdmin)

admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, GeoPageAdmin)