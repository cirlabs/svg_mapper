from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from django.contrib.gis import geos
from django.contrib.gis.geos import fromstr
from django.contrib.gis.gdal import OGRGeometry, OGRGeomType

class Wisconsin(models.Model):
    state = models.CharField(max_length=20)
    state_fips = models.CharField(max_length=2)
    geom = models.MultiPolygonField(srid=4269)
    simple_mpoly_utm15n = models.MultiPolygonField(srid=26915, null=True)
    slug = models.SlugField(blank=True)
    objects = models.GeoManager()

    def save(self, **kwargs):
        self.slug = slugify(self.state)
        #self.internal_point = fromstr('POINT(%s %s)' % (self.lon_internal_point, self.lat_internal_point.replace('+', '')))
        if self.geom and isinstance(self.geom, geos.Polygon):
            self.geom = geos.MultiPolygon(self.geom)
            
        super(self.__class__, self).save(**kwargs)

    def __unicode__(self):
        return self.slug
    
    def set_simple_polygons(self, target_field_name='simple_mpoly', tolerance=2, srid=4326):
        """
        Ben Welsh method
        
        Simplifies the source polygons so they don't use so many points.
        
        Provide a tolerance score the indicates how sharply the
        the lines should be redrawn.
        
        Returns True if successful.
        """

        # Fetch the source polygon
        source_field_name = 'geom'
        source = getattr(self, source_field_name)
        # Fetch the target polygon where the result will be saved
        #target_field_name = 'simple_mpoly'
        target = getattr(self, target_field_name)
        # Simplify the source
        simple = source.transform(srid, True).simplify(tolerance, True)
        # If it's a polygon, convert it to a MultiPolygon
        if simple.geom_type == 'Polygon':
            mp = OGRGeometry(OGRGeomType('MultiPolygon'))
            mp.add(simple.wkt)
            target = mp.wkt
        # Otherwise just save out right away
        else:
            target = simple.wkt
            
        # Set the attribute
        setattr(self, target_field_name, target)
        
        # Save out
        self.save()
        return True
        
class WisconsinInterstates(models.Model):
    feature = models.CharField(max_length=80)
    route = models.CharField(max_length=120)
    state_fips = models.CharField(max_length=2)
    state = models.CharField(max_length=2)
    geom = models.LineStringField(srid=4269)
    slug = models.SlugField(blank=True)
    simple_mpoly_utm15n = models.MultiLineStringField(srid=26915,null=True)
    objects = models.GeoManager()
        
    def save(self, **kwargs):
        self.slug = slugify(self.route)
        #self.internal_point = fromstr('POINT(%s %s)' % (self.lon_internal_point, self.lat_internal_point.replace('+', '')))
#         if self.geom and isinstance(self.geom, geos.LineString):
#             self.geom = geos.LineString(self.geom)
            
        super(self.__class__, self).save(**kwargs)

    def __unicode__(self):
        return self.slug

    def set_simple_polylines(self, target_field_name='simple_mpoly', tolerance=2, srid=4326):
        """
        Ben Welsh method
        
        Simplifies the source polygons so they don't use so many points.
        
        Provide a tolerance score the indicates how sharply the
        the lines should be redrawn.
        
        Returns True if successful.
        """

        # Fetch the source polygon
        source_field_name = 'geom'
        source = getattr(self, source_field_name)
        # Fetch the target polygon where the result will be saved
        #target_field_name = 'simple_mpoly'
        target = getattr(self, target_field_name)
        # Simplify the source
        simple = source.transform(srid, True).simplify(tolerance, True)
        # If it's a polyline, convert it to a MultiPolyline
        if simple.geom_type == 'LineString':
            mp = OGRGeometry(OGRGeomType('MultiLineString'))
            mp.add(simple.wkt)
            target = mp.wkt
        # Otherwise just save out right away
        else:
            target = simple.wkt
            
        # Set the attribute
        setattr(self, target_field_name, target)
        
        # Save out
        self.save()
        return True
        
        
class WisconsinCities(models.Model):
    statefp10 = models.CharField(max_length=2)
    placefp10 = models.CharField(max_length=5)
    placens10 = models.CharField(max_length=8)
    geoid10 = models.CharField(max_length=7)
    name10 = models.CharField(max_length=100)
    namelsad10 = models.CharField(max_length=100)
    lsad10 = models.CharField(max_length=2)
    classfp10 = models.CharField(max_length=2)
    pcicbsa10 = models.CharField(max_length=1)
    pcinecta10 = models.CharField(max_length=1)
    mtfcc10 = models.CharField(max_length=5)
    funcstat10 = models.CharField(max_length=1)
    aland10 = models.FloatField()
    awater10 = models.FloatField()
    intptlat10 = models.CharField(max_length=11)
    intptlon10 = models.CharField(max_length=12)
    geom = models.PointField(srid=4326)
    geom_utm15n = models.PointField(srid=26915)
    slug = models.SlugField(blank=True)
    objects = models.GeoManager()
    
    def save(self, **kwargs):
        self.slug = slugify(self.name10)
        self.geom_utm15n = self.geom.transform(26915, True)
        
        super(self.__class__, self).save(**kwargs)

    def __unicode__(self):
        return self.slug