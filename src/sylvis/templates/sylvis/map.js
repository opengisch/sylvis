
////////////////// Utils //////////////////

var geojsonFormat = new ol.format.GeoJSON({dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var sectorColors = [[141,211,199],[255,255,179],[190,186,218],[251,128,114],[128,177,211],[253,180,98]]; // from https://colorbrewer2.org/#type=qualitative&scheme=Set3&n=6

////////////////// Layers definitions //////////////////

var backgroundLayer = new ol.layer.Tile({
  title: "Swisstopo",
  source: new ol.source.XYZ({
    url: 'https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.landeskarte-grau-10/default/current/3857/{z}/{x}/{y}.png'
  })
});

var plotsLayer = new ol.layer.Vector({
  title: "Plots",
  source: new ol.source.Vector({
    features: geojsonFormat.readFeatures(plotsGeojson)
  }),
  style: function(feature, resolution){
    return new ol.style.Style({
      fill: new ol.style.Fill({
        color: [60, 235, 40, 0.5]
      }),
      stroke: new ol.style.Stroke({
        color: [20, 155, 10, 1],
        width: 2,
      }),
      text: new ol.style.Text({
        text: feature.get('name'),
        fill: new ol.style.Fill({color: [20, 155, 10, 1]}),
        stroke: new ol.style.Stroke({color: 'white', width: 2}),
        font: "bold 15px sans-serif"
      })
    });
  }
});

var sectorsLayers = [];
sectorsGeojsons.forEach((sectorsGeojson, idx) => {
  var i=0;
  var sectorsLayer = new ol.layer.Vector({
    title: `Sectors (level ${idx + 1})`,
    type: "base",
    source: new ol.source.Vector({
      features: geojsonFormat.readFeatures(sectorsGeojson)
    }),
    style: function(feature, resolution){
      if(feature.color === undefined) {
        feature.color = sectorColors[i % sectorColors.length];
        i++;
      }
      console.log("test");
      return new ol.style.Style({
        fill: new ol.style.Fill({
          color: [...feature.color, 0.5]
        }),
        stroke: new ol.style.Stroke({
          color: feature.color,
          width: 2,
        }),
        text: new ol.style.Text({
          text: feature.get('name'),
          fill: new ol.style.Fill({color: feature.color}),
          stroke: new ol.style.Stroke({color: 'black', width: 2}),
          font: "bold 20px sans-serif"
        })
      });
    },
    visible: false
  });
  sectorsLayers.push(sectorsLayer);

});
var sectorsGroup = new ol.layer.Group({
  title: 'Sectors',
  layers: sectorsLayers
});


////////////////// Map configuration //////////////////

var map = new ol.Map({
  target: 'map',
  layers: [
    backgroundLayer,
    plotsLayer,
    sectorsGroup,
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([8.3, 46.9]),
    zoom: 7
  }),
  controls: ol.control.defaults().extend([
    new ol.control.MousePosition(),
    new ol.control.LayerSwitcher()
  ])
});




////////////////// Interactions //////////////////

// let selected = null;
// const status = document.getElementById('status');

// map.on('pointermove', function (e) {
//   if (selected !== null) {
//     selected.setStyle(hiddenStyle);
//     selected = null;
//   }

//   map.forEachFeatureAtPixel(e.pixel, function (f) {
//     selected = f;
//     f.setStyle(highlightStyle);
//     return true;
//   },
//     {
//       layerFilter: function(layer) {return layer === sectorsLayer;}
//   });
// });

////////////////// Initial setup //////////////////

map.getView().fit(plotsLayer.getSource().getExtent());
