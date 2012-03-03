import csv
import os, sys
from django.contrib.gis.utils import LayerMapping
from models import Wisconsin, WisconsinCity, WisconsinInterstate, WisconsinCounty, WisconsinCountyData

#### Data for layer map example #### 
# Auto-generated `LayerMapping` dictionary for Wisconsin model
wisconsin_mapping = {
    'state' : 'STATE',
    'state_fips' : 'STATE_FIPS',
    'geom' : 'MULTIPOLYGON',
}

border_shp = os.path.join('.', 'svg_map/wisconsin/wisconsin.shp')

def run_wisconsin(verbose=True):
    lm = LayerMapping(Wisconsin, border_shp, wisconsin_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)
    
# Auto-generated `LayerMapping` dictionary for WisconsinCity model
wisconsincity_mapping = {
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
        
point_shp = os.path.join('.', 'svg_map/wisconsin_bigger_cities/wisconsin_bigger_cities.shp')

def run_cities(verbose=True):
    lm = LayerMapping(WisconsinCity, point_shp, wisconsincity_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)

# Auto-generated `LayerMapping` dictionary for WisconsinInterstate model
wisconsininterstate_mapping = {
    'feature' : 'FEATURE',
    'route' : 'ROUTE',
    'state_fips' : 'STATE_FIPS',
    'state' : 'STATE',
    'geom' : 'LINESTRING',
}

line_shp = os.path.join('.', 'svg_map/wisconsin_interstates/wisconsin_interstates.shp')

def run_roads(verbose=True):
    lm = LayerMapping(WisconsinInterstate, line_shp, wisconsininterstate_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)

#0.03 tolerance about right for U.S. map in 4326, 3000 about right for lambert, 300 about right for smaller UTM countries
def update_simple_roads():
    for b in WisconsinInterstate.objects.all():
        b.set_simple_polylines('simple_mpoly_utm15n', 300, 26915)
        print '%s simplified' % (b)

#0.03 tolerance about right for U.S. map in 4326, 3000 about right for lambert, 300 about right for smaller UTM countries
def update_simple_polys():
    for b in Wisconsin.objects.all():
        b.set_simple_polygons('simple_mpoly_utm15n', 300, 26915)
        print '%s simplified' % (b)



#### Data for choropleth map example ####        

# Auto-generated `LayerMapping` dictionary for WisconsinCounty model
wisconsincounty_mapping = {
    'statefp10' : 'STATEFP10',
    'countyfp10' : 'COUNTYFP10',
    'countyns10' : 'COUNTYNS10',
    'geoid10' : 'GEOID10',
    'name10' : 'NAME10',
    'namelsad10' : 'NAMELSAD10',
    'lsad10' : 'LSAD10',
    'classfp10' : 'CLASSFP10',
    'mtfcc10' : 'MTFCC10',
    'csafp10' : 'CSAFP10',
    'cbsafp10' : 'CBSAFP10',
    'metdivfp10' : 'METDIVFP10',
    'funcstat10' : 'FUNCSTAT10',
    'aland10' : 'ALAND10',
    'awater10' : 'AWATER10',
    'intptlat10' : 'INTPTLAT10',
    'intptlon10' : 'INTPTLON10',
    'geom' : 'MULTIPOLYGON',
}

county_shp = os.path.join('.', 'svg_map/wisconsin_counties/tl_2010_55_county10.shp')

def run_wisconsin_counties(verbose=True):
    lm = LayerMapping(WisconsinCounty, county_shp, wisconsincounty_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)
    
#0.03 tolerance about right for U.S. map in 4326, 3000 about right for lambert, 300 about right for smaller UTM countries
def update_simple_county_polys():
    for b in WisconsinCounty.objects.all():
        b.set_simple_polygons('simple_mpoly_utm15n', 300, 26915)
        print '%s simplified' % (b)


def load_wisconsin_related_data():
    working_dir = '.'
    data_dir = os.path.join(working_dir, 'svg_map/wisconsin_pop_data')
    file_path = os.path.join(data_dir, 'all_050_in_55.P1.csv')
    handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
    header = handle.next()
    for h in handle:
        try:
            insert = WisconsinCountyData()
            insert.geoid = h[0].strip()
            insert.statefps = h[2].strip()
            insert.countyfps = h[3].strip()
            insert.name = h[8].strip().replace(' County','')
            insert.pop_2010 = h[9].strip()
            insert.pop_2000 = h[11].strip()
            insert.save()
            print h[8].strip()
        except:
            raise

def load_all_sample_data():
    run_wisconsin()
    update_simple_polys()
    run_roads()
    update_simple_roads()
    run_cities()
    run_wisconsin_counties()
    update_simple_county_polys()
    load_wisconsin_related_data()