import math, string
from django.contrib.gis.geos import *

class SVGMap:
    def __init__(self):
        self.geobounds = LatLngBounds()
        self.mapGeoWidth = 0
        self.mapGeoHeight = 0
        self.mapPixelWidth = 1000
        self.mapPixelHeight = 1000
        self.orig_layers = []
        self.svg_layers = []
        self.viewBox = SVGViewBox()
        self.scaleFactor = 1
        self.paddingPct = 0
        self.sigdigs = 7
        self.pixelPadding = 0;
        self.pixelbounds = LatLngBounds()
        
    def updateGeoBounds(self,arrInputPoint):
        #test if this has any new min/max values
        floatXPoint = float(arrInputPoint[0])
        floatYPoint = float(arrInputPoint[1])
        if floatYPoint < self.geobounds.numMinLat:
            self.geobounds.numMinLat = floatYPoint
            
        if floatYPoint > self.geobounds.numMaxLat:
            self.geobounds.numMaxLat = floatYPoint
            
        if floatXPoint < self.geobounds.numMinLng:
            self.geobounds.numMinLng = floatXPoint
            
        if floatXPoint > self.geobounds.numMaxLng:
            self.geobounds.numMaxLng = floatXPoint
        
        self.mapGeoWidth = math.fabs(self.geobounds.numMaxLng - self.geobounds.numMinLng)
        self.mapGeoHeight = math.fabs(self.geobounds.numMaxLat - self.geobounds.numMinLat)
            
    def buildSVGMapViewBox(self):
        #Find maximum bounds to get translation values to make zero-based
        for l in self.orig_layers:
            if l['type'] == 'point':
                for point in l['point_set']:
                    self.updateGeoBounds(point.arrGeometry)
            
            if l['type'] == 'multipolygon':
                for multipolygon in l['multi_set']:
                    for polygon in multipolygon.rings:
                        for key in range(len(polygon.arrGeometry)):
                            point = polygon.arrGeometry[key]
                            if key != len(polygon.arrGeometry)-1:
                                self.updateGeoBounds(point)
                                
            if l['type'] == 'multilinestring':
                for multilinestring in l['multi_set']:
                    for linestring in multilinestring.rings:
                        for key in range(len(linestring.arrGeometry)):
                            point = linestring.arrGeometry[key]
                            self.updateGeoBounds(point)
                        
        self.scaleFactor = self.mapPixelWidth/self.mapGeoWidth
        self.pixelPadding = self.mapPixelWidth*self.paddingPct
        
        self.mapPixelHeight = self.mapGeoHeight*self.scaleFactor
        
        #convert bounds to 0-based values
        self.pixelbounds.numMinLat = 0
        self.pixelbounds.numMinLng = 0
        
        self.pixelbounds.numMaxLat = round(self.mapGeoHeight*self.scaleFactor,self.sigdigs)
        self.pixelbounds.numMaxLng = round(self.mapGeoWidth*self.scaleFactor,self.sigdigs)
        
        self.viewBox.x = round(self.pixelbounds.numMinLng-self.pixelPadding,self.sigdigs)
        self.viewBox.y = round(self.pixelbounds.numMinLat-self.pixelPadding,self.sigdigs)
        self.viewBox.width = round(self.mapPixelWidth+(self.pixelPadding*2),self.sigdigs)
        self.viewBox.height = round(self.mapPixelHeight+(self.pixelPadding*2),self.sigdigs)
        
        return self.viewBox
        
    def translateLayers(self):
        for l in self.orig_layers:
            if (l['type'] == 'point'):
                self.svg_layers.append(SVGPointLayer(self,l['point_set'],l['id']))
            if (l['type'] == 'multilinestring'):
                self.svg_layers.append(SVGLinestringLayer(self,l['multi_set'],l['id']))
            if (l['type'] == 'multipolygon'):
                self.svg_layers.append(SVGPolygonLayer(self,l['multi_set'],l['id']))
        return self.svg_layers
        
    def buildSVGPointLayer(self, layerid, queryset, geomfieldname, idfieldname):
        point_set = []
        for q in queryset:
            #Problems arise when transforming simplified geometries, and too slow with unsimplified. For now better to create a new field in the model.
            #coordinates = getattr(q, geomfieldname).transform(3395, True)
            coordinates = getattr(q, geomfieldname)
            pointid = getattr(q, idfieldname)
            point = Point(coordinates, pointid)
            point_set.append(point)
        self.orig_layers.append({'type':'point','id':layerid,'point_set':point_set})
            
    def buildSVGLinestringLayer(self, layerid, queryset, geomfieldname, idfieldname):
        multi_set = []
        for q in queryset:
            #Problems arise when transforming simplified geometries, and too slow with unsimplified. For now better to create a new field in your preferred projection in the model rather than transforming here.
            #coordinates = getattr(q, geomfieldname).transform(3395, True)
            coordinates = getattr(q, geomfieldname)
            multiid = getattr(q, idfieldname)
            multi = MultiLinestring(coordinates, multiid)
            multi_set.append(multi)
        self.orig_layers.append({'type':'multilinestring','id':layerid,'multi_set':multi_set})

    def buildSVGPolygonLayer(self, layerid, queryset, geomfieldname, idfieldname):
        multi_set = []
        for q in queryset:
            #Problems arise when transforming simplified geometries, and too slow with unsimplified. For now better to create a new field in your preferred projection in the model rather than transforming here.
            #coordinates = getattr(q, geomfieldname).transform(3395, True)
            coordinates = getattr(q, geomfieldname)
            multiid = getattr(q, idfieldname)
            multi = MultiPolygon(coordinates, multiid)
            multi_set.append(multi)
        self.orig_layers.append({'type':'multipolygon','id':layerid,'multi_set':multi_set})
    
    def drawSVGPoint(self,point):
        point_geom = point.arrGeometry
        xpoint = round(self.scaleFactor*(0 - self.geobounds.numMinLng + float(point_geom[0])),self.sigdigs)
        ypoint = round(self.scaleFactor*((math.fabs(self.geobounds.numMaxLat)) - float(point_geom[1])),self.sigdigs)
        return [xpoint,ypoint]
        
    def drawSVGLinestring(self,Linestring):
        paths = []
        for key in range(len(Linestring.arrGeometry)):
            point = Linestring.arrGeometry[key]

            xpoint = round(self.scaleFactor*(0 - self.geobounds.numMinLng + float(point[0])),self.sigdigs)
            ypoint = round(self.scaleFactor*((math.fabs(self.geobounds.numMaxLat)) - float(point[1])),self.sigdigs)
            paths.append(str(xpoint) + ',' + str(ypoint))
        strSVGPath = 'M' + string.join(paths,'L')
        
        return strSVGPath
        
    def drawSVGPolygon(self,polygon):
        paths = []
        for key in range(len(polygon.arrGeometry)):
            point = polygon.arrGeometry[key]

            if key != len(polygon.arrGeometry)-1:
                xpoint = round(self.scaleFactor*(0 - self.geobounds.numMinLng + float(point[0])),self.sigdigs)
                ypoint = round(self.scaleFactor*((math.fabs(self.geobounds.numMaxLat)) - float(point[1])),self.sigdigs)
                paths.append(str(xpoint) + ',' + str(ypoint))
        strSVGPath = 'M' + string.join(paths,'L') + 'Z'
        
        return strSVGPath
        
                
class SVGPointLayer:
    def __init__(self,map,pointlist,identifier=''):
        self.type = 'point'
        self.identifier = identifier
        self.geometries = []
        for point in pointlist:
            point_string = ''
            svgpoint = map.drawSVGPoint(point)
            self.geometries.append({'id':point.identifier,'svgpoint':svgpoint})
        
class SVGLinestringLayer:
    def __init__(self,map,multilinestringlist,identifier=''):
        self.type = 'multilinestring'
        self.identifier = identifier
        self.geometries = []
        for multilinestring in multilinestringlist:
            multi_poly_string = ''
            for ring in multilinestring.rings:
                svgpath = map.drawSVGLinestring(ring)
                multi_poly_string += svgpath
            self.geometries.append({'id':string.replace(multilinestring.identifier,'-','_'),'svgstring':multi_poly_string})

class SVGPolygonLayer:
    def __init__(self,map,multipolygonlist,identifier=''):
        self.type = 'multipolygon'
        self.identifier = identifier
        self.geometries = []
        for multipolygon in multipolygonlist:
            multi_poly_string = ''
            for ring in multipolygon.rings:
                svgpath = map.drawSVGPolygon(ring)
                multi_poly_string += svgpath
            self.geometries.append({'id':string.replace(multipolygon.identifier,'-','_'),'svgstring':multi_poly_string})

class Point:
    def __init__(self, arrInputPoint, identifier=''):
        self.arrGeometry = arrInputPoint
        self.identifier = identifier
        
class Linestring:
    def __init__(self, arrInputPoints, identifier='', identifierkey=''):
        self.arrGeometry = arrInputPoints
        self.identifier = '%s-%s' % (identifier, identifierkey)

class Polygon:
    def __init__(self, arrInputPoints, identifier='', identifierkey=''):
        self.arrGeometry = arrInputPoints
        self.identifier = '%s-%s' % (identifier, identifierkey)

class MultiLinestring:
    def __init__(self, arrInputMultiLinestring, identifier=''):
        self.arrGeometry = arrInputMultiLinestring
        self.identifier = identifier
        self.rings = []
        for key in range(len(arrInputMultiLinestring)):
           self.rings.append(Linestring(arrInputMultiLinestring[key],identifier,key))

class MultiPolygon:
    def __init__(self, arrInputMultiPolygon, identifier=''):
        self.arrGeometry = arrInputMultiPolygon
        self.identifier = identifier
        self.rings = []
        for key in range(len(arrInputMultiPolygon)):
           self.rings.append(Polygon(arrInputMultiPolygon[key][0],identifier,key))

class LatLngBounds:
    def __init__(self, numMinLat=float('inf'), numMaxLat=float('-inf'), numMinLng=float('inf'), numMaxLng=float('-inf')):
        self.numMinLat = numMinLat
        self.numMaxLat = numMaxLat
        self.numMinLng = numMinLng
        self.numMaxLng = numMaxLng

class SVGViewBox:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 10
        self.height = 10