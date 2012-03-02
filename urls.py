from django.conf.urls.defaults import patterns, include, url
from env_settings import STATIC_SERVE_PATH

urlpatterns = patterns('',

    url(r'^json/map/$', 'svg_map.views.layer_map_json', name='layer_map_json'),
    
    #url(r'^json/locatormap/(?P<slug>[\w-]+)/$', 'svg_map.views.locator_map', name='locator_map'),

    url(r'^$', 'svg_map.views.index', name='index'),

)
