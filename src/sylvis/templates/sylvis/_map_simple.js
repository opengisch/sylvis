////////////////// Utils //////////////////

var geojsonFormat = new ol.format.GeoJSON({dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});

////////////////// Layers definitions //////////////////

var backgroundLayer = new ol.layer.Tile({
  title: "Swisstopo",
  source: new ol.source.XYZ({
    url: 'https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.landeskarte-grau-10/default/current/3857/{z}/{x}/{y}.png',
    maxZoom: 19
  })
});

var featureLayer = new ol.layer.Vector({
  source: new ol.source.Vector({
    features: geojsonFormat.readFeatures(featuresGeojson)
  }),
  style: function(feature, resolution){
    return new ol.style.Style({
      fill: new ol.style.Fill({
        color: [60, 235, 40, 0.5]
      }),
      stroke: new ol.style.Stroke({
        color: [20, 155, 10, 1],
        width: 2,
      })
    });
  }
});

////////////////// Map configuration //////////////////

var map = new ol.Map({
  target: 'map',
  layers: [backgroundLayer, featureLayer],
  view: new ol.View({
    center: ol.proj.fromLonLat([8.3, 46.9]),
    zoom: 7
  }),
  controls: []
});


////////////////// Initial setup //////////////////

map.getView().fit(featureLayer.getSource().getExtent());
