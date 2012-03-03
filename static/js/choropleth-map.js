var strServerRoot = '/';

//Set your actual desired final width here. The height will be adjusted based on your map layers.
var numMainMapWidth = 570;
var numMainMapHeight;
var numMapHorizPadding = 75;
var numMapVerticalPadding = 0;

//Used to translate the SVG dimensions to your desired final width/height, and to scale type or other sizes
var numMainMapScale;

var objMainMap;
var objMainMapSet = {};
var arrMapSets = [];

var objLoadElements = {};
objLoadElements.data = false;
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
		
		//categorize related data into color information by getting range of related data
		var numDataMin = null;
		var numDataMax = null;
		var numQuantiles = 8;
		var strDataField = 'poppctchange';
		$.each(objRelatedData, function(numKey, objData) {
 			if (numDataMin === null || objData[strDataField] < numDataMin) {
 				numDataMin = objData[strDataField];
 			}
 			if (numDataMax === null || objData[strDataField] > numDataMax) {
 				numDataMax = objData[strDataField];
 			}
 		});
 		var numQuantileInterval = (numDataMax-numDataMin)/numQuantiles;
 		var arrQuantileMins = [];
 		for (numQ=0; numQ<numQuantiles; numQ++){
 			arrQuantileMins.push(numDataMin + (numQ*numQuantileInterval));
 		}
 		var arrFills = ['#EEE', '#DDD', '#CCC', '#AAA', '#999', '#777', '#666', '#333'];
		
		$.each(objMainMapData, function(numLayerKey, objLayer) {

			//loop through geometries
			$.each(objLayer.geometries, function(numGeomKey, objGeom) {
	
				//match map data to related data
				var objMatch;
				$.each(objRelatedData, function(numDataKey, objExtraData) {
					if (objExtraData.id == parseFloat(objGeom.id)) {
						objMatch = objExtraData;
					}
				});
				
				var strGeomFill = '#FFF';
				$.each(arrQuantileMins, function(numQKey, numQMax) {
					if (objMatch[strDataField] >= numQMax)	{
						strGeomFill = arrFills[numQKey];
					}
				});
				
				//Multipolygon layer style
				var objAttr = {
					"fill": strGeomFill,
					"stroke": "#FFF",
					"stroke-width": 1*numMainMapScale,
					"stroke-linejoin": "round",
					"cursor":"pointer"
				};

				objMainMapSet[objGeom.id] = objMainMap.path(objGeom.svgstring).attr(objAttr)
					.data('slug',objGeom.id)
					.data('main-color',strGeomFill)
					.mouseover(function() {
						this.attr("fill","#EEE");
						})
					.mouseout(function() {
						this.attr("fill",this.data('main-color'));
						})
					.click(function () {
							showDetails(objGeom,objMatch);
						});
					
			});
		});
								
		arrMapSets = [objMainMapSet];
		objMainMap.setViewBox(arrMainMapViewBox[0], arrMainMapViewBox[1], arrMainMapViewBox[2] + numMapHorizPadding*numMainMapScale, arrMainMapViewBox[3], false);

	}
}

function showDetails(objGeom,objMatch) {
	alert(objMatch.name + ' County: ' + objMatch.poppctchange + '% change');
}


function loadMap(strTargetCanvas) {
	
	$.getJSON(strServerRoot + 'json/county/population/', function(data) {
		
		objRelatedData = data.counties;
		objLoadElements.data = true;
		buildMap(strTargetCanvas);
		
	});

	
	$.getJSON(strServerRoot + 'json/choropleth/', function(data) {
		arrMainMapViewBox = data.viewbox;
		objMainMapData = data.layers;
				
		objLoadElements.mainmap = true;
		buildMap(strTargetCanvas);
	
	});
	
 }