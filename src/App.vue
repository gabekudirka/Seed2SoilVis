<template>
  <div id="page">
    <ListContainer class="left-sidebar sidebars" :fleetObj="fleetObj" :tripsObj="tripsObj" :deptsObj="deptsObj"/>
    <div class="main-panel">
      <div class="top-main">
        <MapPanel class="MAP panel" :planObj="planBusObj"> </MapPanel>
        <!-- <PlanDetails class="right-sidebar panel"/> -->
      </div>
      <BusPanel v-if="showVehicles" :fleetObj="fleetObj" :tripsObj="tripsObj" :deptsObj="deptsObj" class="bottom-main panel"/>
      <DeptPanel v-if="!showVehicles" :fleetObj="fleetObj" :tripsObj="tripsObj" :deptsObj="deptsObj" class="bottom-main panel"/>
    </div>
  </div>
</template>

<script>
import BusPanel from './components/BusPanel.vue';
import DeptPanel from './components/DeptPanel.vue';
import MapPanel from './components/MapPanel.vue';
import PlanDetails from './components/PlanDetails.vue';
import ListContainer from './components/ListContainer.vue';
import vehicles from './data/vehicle_details/fleet_details.json';
import tripData from './data/trip_data/trips_9-27_9-29.json';
import departments from './data/vehicle_details/depts_9-27_9-29.json';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  name: 'App',
  components: {
    BusPanel,
    DeptPanel,
    MapPanel,
    // PlanDetails,
    ListContainer
  },
  data() {
    return {
      fleetObj: vehicles,
      tripsObj: tripData,
      deptsObj: departments,
    };
  },
  computed: {
    plan: function () {
      return this.$store.state.plan;
    },
    showVehicles: function () {
      return this.$store.state.showVehicles;
    },
    stateSelectedVehicle: function () {
      return this.$store.state.selectedVehicle;
    },
    stateSelectedDept: function () {
      return this.$store.state.selectedDept;
    },
  },
  mounted() {
    const trips = this.tripsObj.trips.filter(trip => trip.vehicle === this.stateSelectedVehicle);
    this.$store.dispatch('changeSelectedTrips', trips);
  }
};
</script>

<style>
body{
  background-color: #e8f3f2;
}
.sidebars {
  background-color: #efefef;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-size: 11pt;
}
#page{
  display:flex;
  flex-direction:row;
  height: 100vh;
}
.left-sidebar{
  width:20vw;
  flex:1;
  overflow-y:auto;
  height:100%;
  position: fixed;
  z-index:1;
  top: 0;
  left: 0;
}
.panel{
  background-color: #fff;
  margin: .25em;
  padding: .25em;
  filter: drop-shadow(1px 1px 3px #dfdfdf);
  border-radius: 5px;
}
.main-panel{
  flex:3;
  display:flex;
  flex-direction:column;
  margin-left: 20vw;
}
.top-main{
  flex:4;
  display: flex;
  max-height: 62vh;
}
.bottom-main{
  flex:1;
  max-height: 38vh;
  overflow-y: auto;
  overflow-x: hidden;
  z-index: 0;
}
.right-sidebar{
  flex:1;
  max-width: 15vw; 
  overflow-y: auto;
  overflow-x: hidden;
}
.MAP{
  flex:3;
}
.bottom-border{
  border-bottom: 1px solid grey;
}
</style>
