var strServerRoot = '/';

var numMainMapWidth = 570;
var numMainMapHeight;
var numMapHorizPadding = 75;
var numMapVerticalPadding = 0;

var numMainMapScale;

var objMainMap;
var objMainMapSet = {};

var arrMapSets = [];

var boolMapLoaded = false;
var boolDataLoaded = false;

var objLoadElements = {};
//objLoadElements.data = false;
objLoadElements.mainmap = false;

var objMainMapData = null;
var arrMainMapViewBox = null;
var objRelatedData = null;

var strSelectedGeom = null;

function getScaleFactor(numPaperWidth,numViewboxWidth) {
	var numScaleFactor = numViewboxWidth/numPaperWidth;
	return numScaleFactor;
}

function buildMap(strTargetCanvas) {
	var boolAllLoaded = true;
	$.each(objLoadElements, function(numK, objV) {
		if (objV == false) {
			boolAllLoaded = false;
		}
	});
	
	if (boolAllLoaded) {	
				
		//figure proportional size based on viewbox
		numMainMapHeight = (numMainMapWidth*arrMainMapViewBox[3])/arrMainMapViewBox[2];
		
		objMainMap = Raphael(strTargetCanvas, numMainMapWidth, numMainMapHeight);

		//set scale factors
		numMainMapScale = getScaleFactor(numMainMapWidth,arrMainMapViewBox[2] + (numMapHorizPadding*2));
				
		objMainMapSet = {};
		
		$.each(objMainMapData, function(numLayerKey, objLayer) {
			//Multipolygon layers
			if (objLayer.type == 'multipolygon') {
				
				//Multipolygon layer style
				var objAttr = {
					fill: "#D1D3D4",
					stroke: "none",
					"stroke-linejoin": "round"
				};
		
				//loop through geometries
				$.each(objLayer.geometries, function(numGeomKey, objGeom) {
		
					objMainMapSet[objGeom.id] = objMainMap.path(objGeom.svgstring).attr(objAttr)
						.data('slug',objGeom.id);
					
				}); 			
			}
			
			if (objLayer.type == 'multilinestring') {

				//Multilinestring layer style
				var objLineAttr = {
					"stroke": "#999",
					"stroke-width": 1*numMainMapScale
				};			
				
				$.each(objLayer.geometries, function(numGeomKey, objGeom) {
		
					objMainMapSet[objGeom.id] = objMainMap.path(objGeom.svgstring).attr(objLineAttr)
						.data('slug',objGeom.id);
						
				});		
			}
			
			if (objLayer.type == 'point') {
				
				//Point layer style
				var objCircleAttr = {
					"fill": "#0D8140",
					"stroke": "#FFFFFF",
					"stroke-width": 1.5,
					"stroke-linejoin": "round",
					"cursor": "pointer"
				};
				
				var numPixelTypeSize = 12*numMainMapScale;
				
				$.each(objLayer.geometries, function(numGeomKey, objGeom) {
		
					objMainMapSet[objGeom.id] = objMainMap.circle(objGeom.svgpoint[0], objGeom.svgpoint[1], 8*numMainMapScale).attr(objCircleAttr)
						.data('slug',objGeom.id)
						.mouseover(function () {
							showDetails(objGeom.id);
						});			
				});		
			}
		});
								
		arrMapSets = [objMainMapSet];
		objMainMap.setViewBox(arrMainMapViewBox[0], arrMainMapViewBox[1], arrMainMapViewBox[2] + numMapHorizPadding*numMainMapScale, arrMainMapViewBox[3], false);

	}
}

function showDetails(strSlug) {
	alert(strSlug);
}


function loadMap(strTargetCanvas) {
	
	$.getJSON(strServerRoot + 'facility/all/json/', function(data) {
		
// 		objRelatedData = data;
// 		objLoadElements.data = true;
// 		buildMap(strTargetCanvas);
		
	});

	
	$.getJSON(strServerRoot + 'json/map/', function(data) {
		arrMainMapViewBox = data.viewbox;
		objMainMapData = data.layers;
				
		objLoadElements.mainmap = true;
		buildMap(strTargetCanvas);
	
	});
	
 }