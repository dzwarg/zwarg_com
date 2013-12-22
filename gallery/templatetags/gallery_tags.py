from mezzanine.galleries.models import Gallery, GalleryImage

from django.db.models import Count, Q
from mezzanine import template

register = template.Library()

@register.as_tag
def gallery_recent_galleries(limit=5):
    """
    Put a list of recently published galleries into the template
    context.

    Derived from "blog_recent_posts" in the blog module.

    Usage::

        {% gallery_recent_galleries 5 as recent_galleries %}
    """
    galleries = Gallery.objects.published()
    return list(galleries[:limit])

@register.as_tag
def gallery_recent_images(limit=5):
    """
    Put a list of recently published gallery images into the template
    context.

    Derived from "gallery_recent_galleries" in the geo module.

    Usage::

        {% gallery_recent_images 5 as recent_images %}
    """
    images = GalleryImage.objects.all().order_by('-id')
    return list(images[:limit])