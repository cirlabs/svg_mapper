from django.shortcuts import get_object_or_404, Http404, render_to_response
from svg_map.models import Wisconsin, WisconsinCities, WisconsinInterstates
from svg_map.svgmap import *
from django.template import RequestContext

def map_json(request):
    statelist = Wisconsin.objects.all()
    city_list = WisconsinCities.objects.all()
    road_list = WisconsinInterstates.objects.all()
    
    themap = SVGMap()
    themap.mapPixelWidth = 1000
    themap.paddingPct = 0.01
    themap.sigdigs = 4
    
    #polygon layer
    themap.buildSVGPolygonSet(statelist, 'simple_mpoly_utm15n', 'state_fips')
    
    #polyline layer
    themap.buildSVGLinestringSet(road_list, 'simple_mpoly_utm15n', 'feature')

    #point layer
    themap.buildSVGPointSet(city_list, 'geom_utm15n', 'slug')
    
    viewbox = themap.buildSVGMapViewBox()
    map_layers = []
    map_layers.append(SVGPolygonLayer(themap,themap.multipolygons,'wi_border'))
    map_layers.append(SVGLinestringLayer(themap,themap.multilinestrings,'wi_roads'))
    map_layers.append(SVGPointLayer(themap,themap.points,'wi_cities'))
    
    return render_to_response('svg.json', {
        'viewbox': viewbox,
        'map_layers': map_layers,
        },
        context_instance=RequestContext(request))


# def locator_map(request, slug):
#     statelist = USAStates.objects.filter(slug='california')
#     facility_list = Facility.objects.filter(slug=slug)
#     
#     themap = SVGMap()
#     #themap.mapPixelWidth = 475
#     themap.mapPixelWidth = 1000
#     themap.paddingPct = 0.01
#     themap.sigdigs = 2
#     
#     #polygon layer
#     themap.buildSVGPolygonSet(statelist, 'simple_mpoly_caplane', 'state_fips')
#     #viewbox = themap.buildSVGMapViewBox()
#     #print viewbox.x
#     
#     #point layer
#     themap.buildSVGPointSet(facility_list, 'geom_caplane', 'slug')
#     
#     viewbox = themap.buildSVGMapViewBox()
#     multipoly_paths = themap.SVGPolygonSet(themap.multipolygons)
#     point_paths = themap.SVGPointSet(themap.points)
#     
#     return render_to_response('svg.json', {
#         'viewbox': viewbox,
#         'svg_multipoly_paths': multipoly_paths,
#         'svg_point_paths': point_paths,
#         },
#         context_instance=RequestContext(request))
        
def index(request):
    
    return render_to_response('basiclayermap.html', {
        },
        context_instance=RequestContext(request))