/* eslint-disable func-names */
/* eslint-disable */
<template>
  <div>
    <div id="mapContainer" ref="mapElement">
  </div>
  </div>
</template>

<script>
import { toRaw } from 'vue';
import 'leaflet/dist/leaflet.css';
import 'leaflet-control-geocoder/dist/Control.Geocoder.css';
import L from 'leaflet';
import 'leaflet.markercluster';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'heatmap.js';
import HeatmapOverlay from 'heatmap.js/plugins/leaflet-heatmap';
import voronoi from '@turf/voronoi';
import bbox from '@turf/bbox';
import idleContour from '../data/trip_data/idle_contour.json';
import pollutantConcentrations from '../data/supplementary_data/pollutant_concentrations.json';
import stopMarker from '../assets/images/orange_icon2.png';
import heatmapDataJson from '../data/trip_data/heatmap_data.json';

export default {
  name: 'BusMap',
  data() {
    return {
      center: [40.7608, -111.891],
      zoom: 12,
      map: null,
      economicLegend: this.createLegend('economic'),
      pollutantLegend: this.createLegend('pollutant'),
    };
  },
  computed: {
    stateSelectedVehicle: function () {
      return this.$store.state.selectedVehicle;
    },
    fromDate: function () {
      return this.$store.state.fromDate;
    },
    toDate: function () {
      return this.$store.state.toDate;
    },
    selectedTrips: function () {
      return this.$store.state.selectedTrips;
    },
    stopIcon: function () {
      return L.icon({
        iconUrl: stopMarker,
        iconSize: [26, 26],
        iconAnchor: [13, 26]
      });
    },
    heatmapData: function () {
      return {
        max: Math.max(...heatmapDataJson.stops.map(el => el.idle_duration)),
        data: heatmapDataJson.stops
      };
    },
  },
  watch: {
    // Update the map whenever the dates or selected vehicle/department changes
    fromDate: function () {
      this.markerCluster.clearLayers();
      this.drawStops();
    }, 
    toDate: function () {
      this.markerCluster.clearLayers();
      this.drawStops();
    }, 
    stateSelectedVehicle: function () {
      this.markerCluster.clearLayers();
      this.drawStops();
    }, 
    selectedTrips: function () {
      if (this.markerCluster) {
        this.markerCluster.clearLayers();
      } 
      
      this.drawStops();
    }, 
  },
  methods: {
    drawMap() {
      const osmMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      });

      const googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
          subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
      });

     this.map = L.map(this.$refs.mapElement, {
        center: this.center,
        layers: [googleSat, osmMap],
        zoom: this.zoom,
        doubleClickZoom: false,
      });

      const pollutantConcentrationOverlay = this.drawPollutantConcentrationOverlay();

      // Add the heatmap overlays
      const idleHeatmapConfig = {
        radius: 0.005,
        maxOpacity: 5,
        scaleRadius: true,
        useLocalExtrema: true,
        latField: 'lat',
        lngField: 'lng',
        valueField: 'idle_duration'
      };
      const idleHeatmapLayer = new HeatmapOverlay(idleHeatmapConfig);
      const idleHeatmap = idleHeatmapLayer;

      const stopsHeatmapConfig = {
        radius: 0.002,
        maxOpacity: 5,
        scaleRadius: true,
        useLocalExtrema: true,
        latField: 'lat',
        lngField: 'lng',
        valueField: 'stopped_duration'
      };
      const stopsHeatmapLayer = new HeatmapOverlay(stopsHeatmapConfig);
      const stopsHeatmap = stopsHeatmapLayer;

      const overlays = {
        'Pollutant Concentrations': pollutantConcentrationOverlay,
        'Idle Time Heatmap': idleHeatmap,
        'Stops Heatmap': stopsHeatmap,
      };

      const baseMaps = {
        'Google Sattelite': googleSat,
        'Open Street Maps': osmMap,
      };

      L.control.layers(baseMaps, overlays).addTo(this.map);

      idleHeatmapLayer.setData(this.heatmapData);
      stopsHeatmapLayer.setData(this.heatmapData);

      this.map.on('overlayadd', (e) => {
        if (e.name === 'Pollutant Concentrations') {
          this.pollutantLegend.addTo(this.map);
          this.info.addTo(this.map);
        }
      });
      this.map.on('overlayremove', (e) => {
          if (e.name === 'Pollutant Concentrations') {
          this.pollutantLegend.remove();
        }
      });
    },
    drawPollutantConcentrationOverlay() {
      const ref = this;

      const pollutantBbox = bbox(pollutantConcentrations);
      const pollutantsVoronoi = voronoi(pollutantConcentrations, { pollutantBbox });
      pollutantsVoronoi.features.forEach((feature, i) => {
        feature.properties.PM25 = pollutantConcentrations.features[i].properties.PM25;
      });

      pollutantConcentrations.features.forEach((feature, i) => {
        if (pollutantsVoronoi.features[i]) {
          pollutantsVoronoi.features[i].properties.PM25 = feature.properties.PM25;
        } else {
          pollutantsVoronoi.features[i] = {
            geometry: {
                coordinates: [
                    [[0, 0], [0, 0], [0, 0], [0, 0]]
                ],
                type: 'Polygon'
            },
            properties: {
                PM25: '0'
            },
            type: 'Feature'
          };
        }
      });

      const onEachFeature = function (feature, layer) {
        layer.on({
            mouseover: ref.highlightFeature,
            mouseout: function (e) {
              pollutantConcentrationOverlay.resetStyle(e.target);
              ref.info.hide();
            },
        });
      };

      function pollutantOverlayStyle(feature) {
        return {
          fillColor: ref.getColor([0, 5, 10, 15, 20, 25, 30, 35], feature.properties.PM25),  
          weight: 1,
          opacity: 0.6,
          color: 'black',
          fillOpacity: 0.5,
        };
      }
      
      const pollutantConcentrationOverlay = L.geoJson(pollutantsVoronoi, {
        style: pollutantOverlayStyle,
        onEachFeature: onEachFeature
      });

      return pollutantConcentrationOverlay;
    },
    getColor(range, bracket1, bracket2 = 0, totalHouseholds = 1) {
      if (totalHouseholds === 0) {
        return '#fffefa';
      }
        
      const b = parseFloat(bracket1) + parseFloat(bracket2);
      return b > range[7] ? '#800026'
            : b > range[6] ? '#BD0026'
            : b > range[5] ? '#E31A1C'
            : b > range[4] ? '#FC4E2A'
            : b > range[3] ? '#FD8D3C'
            : b > range[2] ? '#FEB24C'
            : b > range[1] ? '#FED976'
            : b > range[0] ? '#FFEDA0'
            : '#fff7d6';
    },
    highlightFeature(e) {
      const layer = e.target;
      layer.setStyle({
          weight: 3,
          color: '#666',
          dashArray: '',
          fillOpacity: 0.7
      });

      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }

      this.info.show(layer); 
    },
    createLegend(overlayType) {
      const ref = this;
      const legend = L.control({ position: 'bottomleft' });

      legend.onAdd = function (map) {
          const div = L.DomUtil.create('div', 'info legend');

          if (overlayType === 'economic') {
            const grades = [0, 10, 20, 30, 40, 50, 60, 70]; 
            div.innerHTML = '<p><b>Households making </br> less than $50,000</b></p>';
            for (let i = 0; i < grades.length; i++) {
                div.innerHTML += '<i style="background:' + ref.getColor(grades, grades[i] + 1) + '"></i> '
                    + grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '%<br>' : '%+');
            }
            return div;
          } else if (overlayType === 'pollutant') {
            const grades = [0, 5, 10, 15, 20, 25, 30, 35]; 
            div.innerHTML = '<p><b>PM2.5 Levels</b></p>';
            for (let i = 0; i < grades.length; i++) {
                div.innerHTML += '<i style="background:' + ref.getColor(grades, grades[i] + 1) + '"></i> '
                    + grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
            }
            return div;
          }
      };
      return legend;
    },
    // Draws and clusters all the stop markers on the map
    drawStops() {
      const ref = this;      
      let timeSelectedTrips = [];
      // Make sure we are only drawing stops in the specified period of time
      if (this.selectedTrips.length > 0) {
        timeSelectedTrips = this.selectedTrips.filter(el => new Date(el.date) >= ref.fromDate && new Date(el.date) <= ref.toDate);
      } 
      const selectedTripsGeojson = [];
      timeSelectedTrips.forEach(trip => {
        if (trip.show) {
          selectedTripsGeojson.push(...trip.geojson);
        }
      });
      function onEachFeature(feature, layer) {
        layer.bindTooltip(`<p><b>Vehicle:</b> ${feature.properties.vehicle}</p>
                           <p><b>Stop Start:</b> ${feature.properties.startTime}</p>
                           <p><b>Stop End:</b> ${feature.properties.endTime}</p>
                           <p><b>Duration:</b> ${feature.properties.stopDuration} minutes</p>
                           <p><b>Idle Duration:</b> ${feature.properties.idleDuration} minutes</p>
                           <p><b>Stop Number:</b> ${feature.properties.stopNum}</p>`);
      }
      const stopMarkers = L.geoJSON(selectedTripsGeojson, {
        pointToLayer: function (feature, latlng) {
             return L.marker(latlng, { icon: ref.stopIcon });
        },
        onEachFeature: onEachFeature,
      });
      this.markerCluster = L.markerClusterGroup();
      this.markerCluster.addLayers(stopMarkers);
      this.markerCluster.addTo(toRaw(this.map));
    }
  },
  mounted() {
    this.drawMap();
    this.drawStops();
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove();
    }
  },
};
</script>

<style scoped>

#mapContainer {
  min-height: 60vh;
  background-color: #fff;
  margin: .25em;
  padding: .25em;
  filter: drop-shadow(1px 1px 3px #dfdfdf);
  flex:5;
}

@media (max-height: 400px) {
  #mapContainer {
    min-height: 45vh;
  }
}
#mapContainer >>> .info {  
  padding: 6px 8px;
  font: 14px/16px Arial, Helvetica, sans-serif;
  border-radius: 5px;
  text-align: left;
  background: #fff;
}
#mapContainer >>> .info h2 {
  margin: 0 0 5px;
  color: #777;
}

#mapContainer >>> .route-tooltip {  
  padding: 4px 4px;
  background: white;
  border-radius: 5px;
  text-align: left;
}

#mapContainer >>> .leaflet-control-layers-base {  
  text-align: left; 
}

#mapContainer >>> .leaflet-control-layers-overlays {  
  text-align: left; 
}

#mapContainer >>> .legend {
    line-height: 18px;
    color: #555;
    background: #fff;
}

#mapContainer >>> .legend i {
    width: 18px;
    height: 18px;
    float: left;
    margin-right: 8px;
    opacity: 0.7;
}
</style>
