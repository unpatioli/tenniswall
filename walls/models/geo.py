from django.contrib.gis.db import models as geomodels

class Location(geomodels.Model):
    # GeoDjango fields
    location = geomodels.PointField()

    objects = geomodels.GeoManager()

    class Meta:
        abstract = True