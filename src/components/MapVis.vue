// This file displays the map and map visualizations
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
import stopMarker from '../assets/images/orange_icon2.png';
import heatmapDataJson from '../data/heatmap_data.json';
import pollutantOverlayJson from '../data/pollutant_overlay.json';

export default {
  name: 'BusMap',
  data() {
    return {
      center: [40.7608, -111.891],
      zoom: 12,
      map: null,
      economicLegend: this.createLegend('economic'),
      pollutantLegend: this.createLegend('pollutant'),
      idleHeatmapConfig: {
        radius: 0.005,
        maxOpacity: 5,
        scaleRadius: true,
        useLocalExtrema: true,
        latField: 'lat',
        lngField: 'lng',
        valueField: 'idle_duration'
      },
      selectedIdleHeatmapConfig: {
        radius: 0.005,
        maxOpacity: 5,
        scaleRadius: true,
        useLocalExtrema: true,
        latField: 'lat',
        lngField: 'lng',
        valueField: 'idle_duration'
      }
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
    showVehicles: function () {
      return this.$store.state.showVehicles;
    },
    selectedVehicle: function () {
      return this.$store.state.selectedVehicle;
    },
    selectedDept: function () {
      return this.$store.state.selectedDept;
    },
    stopIcon: function () {
      return L.icon({
        iconUrl: stopMarker,
        iconSize: [26, 26],
        iconAnchor: [13, 26]
      });
    },
    // Load heatmap data for all devices in the correct format
    heatmapData: function () {
      return {
        max: Math.max(...heatmapDataJson.stops.map(el => el.idle_duration)),
        data: heatmapDataJson.stops
      };
    },
    // Load heatmap data for the selected vehicles in the selected time frame
    selectedHeatmapData: function () {
      if (this.showVehicles) {
        const selectedData = heatmapDataJson.stops.filter(el => {
          return el.device === this.selectedVehicle && new Date(el.start_time) >= this.fromDate && new Date(el.end_time) <= this.toDate;
        });
        return {
          max: Math.max(...selectedData.map(el => el.idle_duration)),
          data: selectedData
        }; 
      } else {
        const selectedData = heatmapDataJson.stops.filter(el => {
          return el.group === this.selectedDept && new Date(el.start_time) >= this.fromDate && new Date(el.end_time) <= this.toDate;
        });
        return {
          max: Math.max(...selectedData.map(el => el.idle_duration)),
          data: selectedData
        }; 
      }
    },
    selectedIdleHeatmapLayer: function () {
      return new HeatmapOverlay(this.selectedIdleHeatmapConfig);
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
      this.selectedIdleHeatmapLayer.setData(this.selectedHeatmapData);
    }, 
    selectedTrips: function () {
      if (this.markerCluster) {
        this.markerCluster.clearLayers();
      } 
      
      this.drawStops();
      this.selectedIdleHeatmapLayer.setData(this.selectedHeatmapData);
    }, 
  },
  methods: {
    drawMap() {
      const osmMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      });

      // Google satellite background map option. Removed due to slow rendering
      // const googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
      //     subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
      // });

     this.map = L.map(this.$refs.mapElement, {
        center: this.center,
        // layers: [googleSat, osmMap],
        layers: [osmMap],
        zoom: this.zoom,
        doubleClickZoom: false,
      });

      const img = pollutantOverlayJson.overlay_img;

      const bnd = [[41.384924, -112.467771], [39.961038, -111.179579]];
      const krigLayer = L.imageOverlay(img, bnd, { opacity: 0.7 });

      // Add the heatmap overlays
      const idleHeatmapLayer = new HeatmapOverlay(this.idleHeatmapConfig);
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
        'Pollutant Concentrations': krigLayer,
        'Idle Time Heatmap': idleHeatmap,
        'Selection Idle Time Heatmap': this.selectedIdleHeatmapLayer,
        'Stops Heatmap': stopsHeatmap,
      };

      const baseMaps = {
        // 'Google Sattelite': googleSat,
        'Open Street Maps': osmMap,
      };

      L.control.layers(baseMaps, overlays).addTo(this.map);

      idleHeatmapLayer.setData(this.heatmapData);
      this.selectedIdleHeatmapLayer.setData(this.selectedHeatmapData);
      stopsHeatmapLayer.setData(this.heatmapData);

      // Add and remove the legend when the pollutant concentrations overlay is visible
      this.map.on('overlayadd', (e) => {
        if (e.name === 'Pollutant Concentrations') {
          this.pollutantLegend.addTo(this.map);
          // this.info.addTo(this.map);
        } else if (e.name === 'Selection Idle Time Heatmap') {
          // this.selectedIdleHeatmapLayer.setData(this.selectedHeatmapData);
        }
      });
      this.map.on('overlayremove', (e) => {
          if (e.name === 'Pollutant Concentrations') {
          this.pollutantLegend.remove();
        }
      });
    },
    // Get colors for pollutant concentration legend
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
    // Draw the legend
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
