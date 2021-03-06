from models import Path
from django.contrib.gis import admin as gis_admin
from django.contrib import admin

from copy import deepcopy
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import Page, RichTextPage
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost

gis_admin.site.register(Path, gis_admin.OSMGeoAdmin)

page_fieldsets = deepcopy(PageAdmin.fieldsets)
page_fieldsets[0][1]["fields"] += ('content', 'geom',)

class GeoPageAdmin(PageAdmin):
    fieldsets = page_fieldsets

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"] += ('geom',)

class GeoBlogAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets

admin.site.unregister(Page)
admin.site.register(Page, GeoPageAdmin)

admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, GeoPageAdmin)

admin.site.unregister(BlogPost)
admin.site.register(BlogPost, GeoBlogAdmin)