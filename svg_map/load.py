import os
from django.contrib.gis.utils import LayerMapping
from models import Wisconsin, WisconsinCities, WisconsinInterstates

# Auto-generated `LayerMapping` dictionary for Wisconsin model
wisconsin_mapping = {
    'state' : 'STATE',
    'state_fips' : 'STATE_FIPS',
    'geom' : 'MULTIPOLYGON',
}

border_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '/Users/michaelcorey/Documents/virtual-environments/svg_mapper/project/svg_mapper/svg_map/wisconsin/wisconsin.shp'))

def run_wisconsin(verbose=True):
    lm = LayerMapping(Wisconsin, border_shp, wisconsin_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)
    
# Auto-generated `LayerMapping` dictionary for WisconsinCities model
wisconsincities_mapping = {
    'statefp10' : 'STATEFP10',
    'placefp10' : 'PLACEFP10',
    'placens10' : 'PLACENS10',
    'geoid10' : 'GEOID10',
    'name10' : 'NAME10',
    'namelsad10' : 'NAMELSAD10',
    'lsad10' : 'LSAD10',
    'classfp10' : 'CLASSFP10',
    'pcicbsa10' : 'PCICBSA10',
    'pcinecta10' : 'PCINECTA10',
    'mtfcc10' : 'MTFCC10',
    'funcstat10' : 'FUNCSTAT10',
    'aland10' : 'ALAND10',
    'awater10' : 'AWATER10',
    'intptlat10' : 'INTPTLAT10',
    'intptlon10' : 'INTPTLON10',
    'geom' : 'POINT',
}
        
point_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '/Users/michaelcorey/Documents/virtual-environments/svg_mapper/project/svg_mapper/svg_map/wisconsin_bigger_cities/wisconsin_bigger_cities.shp'))

def run_cities(verbose=True):
    lm = LayerMapping(WisconsinCities, point_shp, wisconsincities_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)

# Auto-generated `LayerMapping` dictionary for WisconsinInterstates model
wisconsininterstates_mapping = {
    'feature' : 'FEATURE',
    'route' : 'ROUTE',
    'state_fips' : 'STATE_FIPS',
    'state' : 'STATE',
    'geom' : 'LINESTRING',
}

line_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '/Users/michaelcorey/Documents/virtual-environments/svg_mapper/project/svg_mapper/svg_map/wisconsin_interstates/wisconsin_interstates.shp'))

def run_roads(verbose=True):
    lm = LayerMapping(WisconsinInterstates, line_shp, wisconsininterstates_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)

#0.03 tolerance about right for U.S. map in 4326, 3000 about right for lambert, 300 about right for smaller UTM countries
def update_simple_roads():
    for b in WisconsinInterstates.objects.all():
        b.set_simple_polylines('simple_mpoly_utm15n', 300, 26915)
        print '%s simplified' % (b)

#0.03 tolerance about right for U.S. map in 4326, 3000 about right for lambert, 300 about right for smaller UTM countries
def update_simple_polys():
    for b in Wisconsin.objects.all():
        b.set_simple_polygons('simple_mpoly_utm15n', 300, 26915)
        print '%s simplified' % (b)