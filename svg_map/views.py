from django.shortcuts import get_object_or_404, Http404, render_to_response
from svg_map.models import Wisconsin, WisconsinCity, WisconsinInterstate, WisconsinCounty, WisconsinCountyData
from svg_map.svgmap import *
from django.template import RequestContext

def index(request):
    
    return render_to_response('basiclayermap.html', {
        },
        context_instance=RequestContext(request))

#### view for layer map example ####
def layer_map_json(request):
    #Collect your GeoDjango objects
    statelist = Wisconsin.objects.all()
    city_list = WisconsinCity.objects.all()
    road_list = WisconsinInterstate.objects.all()
    
    themap = SVGMap()
    #The width is somewhat arbitrary since this is all vector. If you're using Raphael, you can set whatever width you want at the JS level, so I rarely change this value here.
    themap.mapPixelWidth = 1000
    themap.paddingPct = 0.01
    #How many digits to round your final points to. This will vary slightly with projection. If you round too low, you'll lose detail. If you don't round at all you're just doing extra math for no reason.
    themap.sigdigs = 4
    
    #build layers in the order you'd like to display them. You could override this at the JS level if you wanted to.
    #polygon layer
    themap.buildSVGPolygonLayer('wi_border', statelist, 'simple_mpoly_utm15n', 'state_fips')

    #polyline layer
    themap.buildSVGLinestringLayer('wi_roads', road_list, 'simple_mpoly_utm15n', 'feature')

    #point layer
    themap.buildSVGPointLayer('wi_cities', city_list, 'geom_utm15n', 'slug')
    
    #Get the maximum extent of all layers
    viewbox = themap.buildSVGMapViewBox()
    #Use the map's extent info to translate all the points to fit inside your pixel width specified above.
    map_layers = themap.translateLayers()
    
    return render_to_response('svg.json', {
        'viewbox': viewbox,
        'map_layers': map_layers,
        },
        context_instance=RequestContext(request))
        
#### Views for choropleth example ####

def choropleth_map_json(request):
    statelist = WisconsinCounty.objects.all()
    
    themap = SVGMap()
    themap.mapPixelWidth = 1000
    themap.paddingPct = 0.01
    themap.sigdigs = 4
    
    themap.buildSVGPolygonLayer('wi_counties', statelist, 'simple_mpoly_utm15n', 'countyfp10')
    
    viewbox = themap.buildSVGMapViewBox()
    map_layers = themap.translateLayers()
    
    return render_to_response('svg.json', {
        'viewbox': viewbox,
        'map_layers': map_layers,
        },
        context_instance=RequestContext(request))

def related_data_json(request):
    county_list = WisconsinCountyData.objects.all()

    return render_to_response('population.json', {
        'county_list': county_list,
        },
        context_instance=RequestContext(request))

def choropleth_html(request):
    
    return render_to_response('choropleth.html', {
        },
        context_instance=RequestContext(request))
