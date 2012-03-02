var strServerRoot = '/';

//Set your actual desired final width here. The height will be adjusted based on your map layers.
var numMainMapWidth = 570;
var numMainMapHeight;
var numMapHorizPadding = 75;
var numMapVerticalPadding = 0;

//Used to translate the SVG dimensions to your desired final width/height, and to scale type or other sizes
var numMainMapScale;

//Used for holding Raphael stuff
var objMainMap;
var objMainMapSet = {};
var arrMapSets = [];

var objLoadElements = {};
objLoadElements.mainmap = false;

var objMainMapData = null;
var arrMainMapViewBox = null;

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
	
	$.getJSON(strServerRoot + 'json/map/', function(data) {
		arrMainMapViewBox = data.viewbox;
		objMainMapData = data.layers;
				
		objLoadElements.mainmap = true;
		buildMap(strTargetCanvas);
	
	});
 }