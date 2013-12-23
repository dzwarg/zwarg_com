from django.contrib.gis.db.models import GeoManager
from django.contrib.sites.managers import CurrentSiteManager as MezzSiteManager
from mezzanine.core.managers import PublishedManager
from mezzanine.utils.sites import current_site_id

class CurrentSiteManager(GeoManager, MezzSiteManager):
    """
    Extends Django's site manager to first look up site by ID stored in
    the request, the session, then domain for the current request
    (accessible via threadlocals in ``mezzanine.core.request``), the
    environment variable ``MEZZANINE_SITE_ID`` (which can be used by
    management commands with the ``--site`` arg, finally falling back
    to ``settings.SITE_ID`` if none of those match a site.
    """
    def __init__(self, field_name=None, *args, **kwargs):
        super(MezzSiteManager, self).__init__(*args, **kwargs)
        self.__field_name = field_name
        self.__is_validated = False

    def get_query_set(self):
        if not self.__is_validated:
            self._validate_field_name()
        lookup = {self.__field_name + "__id__exact": current_site_id()}
        return super(GeoManager, self).get_query_set().filter(**lookup)


class DisplayableGeoManager(CurrentSiteManager, PublishedManager):
    """
    Manually combines ``CurrentSiteManager``, ``PublishedManager``
    and ``SearchableManager`` for the ``Displayable`` model.

    """
    pass
