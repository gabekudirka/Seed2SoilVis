/* eslint-disable */
<template>
    <div class="left-align" style="padding:1em">    
        <div class="row1">
            <div class="left-align flex1 col-3">
                <h4>
                    <!-- <i class="fas fa-bus" style="padding:.1em"></i> -->
                    Vehicle: {{ vehicle.id }} 
                </h4>
                <p> <b> Department: </b> <button class='dept-btn' @click="showDept(vehicle.department)">{{ vehicle.department }}</button></p>
                <p> <b> Make/Model: </b> {{ vehicle.make }} {{ vehicle.model }} </p>
                <p> <b> Class: </b> {{ vehicle.vehicle_class }} </p>
                <p> <b> Year: </b> {{ vehicle.year }} </p>
                <p> <b> Vehicle Status: </b> Parked </p>

            </div>
            <div class="flex1">
                <div id="miles-chart-container" class="chart">
                    <p class="chart-title"> <b> Vehicle Usage </b> </p>
                    <PanelChart
                        :chartData="timeSelectedTrips"
                        :chartName="'vehicleDrivingDuration'"
                        :containerWidth="chartSize.width"
                        :containerHeight="chartSize.height"
                    />
                </div>
            </div>
            <div class="flex1">
                <DateSelect />
                <TripList :tripsObj="tripsObj"/>
            </div>
        </div>
    </div>
</template>

<script>
import PanelChart from './PanelChart.vue';
import stopsList from '../data/allStops.json';
import DateSelect from './DateSelect.vue';
import TripList from './TripList.vue';

export default {
    name: 'BusPanel',
    components: {
        PanelChart,
        DateSelect,
        TripList,
    },
    props: {
        fleetObj: {
            type: Object,
            required: true
        },
        tripsObj: {
            type: Object,
            required: true,
        },
        deptsObj: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            chartSize: {
                height: 250,
                width: 400
            },
            fleet: this.fleetObj.vehicles,
            departments: this.deptsObj.departments,
            allTrips: this.tripsObj.trips
        };
    },
    computed: {
        vehicleId: function () {
            return this.$store.state.selectedVehicle;
        },
        vehicle: function () {
            return this.fleet.find((vehicle) => vehicle.id === this.vehicleId);
        },
        fromDate: function () {
            return this.$store.state.fromDate;
        },
        toDate: function () {
            return this.$store.state.toDate;
        },
        stateSelectedTrips: function () {
            return this.$store.state.selectedTrips;
        },
        showVehiclesState: function () {
            return this.$store.state.showVehicles;
        },
        timeSelectedTrips: function () {
            return this.stateSelectedTrips.filter(trip => new Date(trip.date) >= this.fromDate && new Date(trip.date) <= this.toDate);
        },
    },
    watch: {
        // vehicleId: function () {
        //     this.trips = this.allTrips.filter((trip) => trip.vehicle === this.vehicleId);
        // },
    },
    methods: {
        showDept(deptName) {
            this.$store.dispatch('changeDept', deptName);
            const deptVehicles = this.fleet.filter(vehicle => vehicle.department === deptName).map(vehicle => vehicle.id);
            const selectedTrips = this.allTrips.filter(trip => deptVehicles.includes(trip.vehicle));
            this.$store.dispatch('changeSelectedTrips', selectedTrips);
            this.$store.dispatch('changePanelView', !this.showVehiclesState);
        }
    }
};
</script>

<style>
.row1{
    display: flex;
    flex-direction:row;
    flex-wrap:wrap;
}
.left-align{
    text-align: left;
    padding-left:1em;
}
.flex1{
    flex:1;
}
.chart-title{
    text-align: center;
    font-size: 18px;
}
p{
    margin: 0.2em !important;
}
.chart{
    max-width:31vw;
}
.dept-btn {
  border: none;
  background-color: inherit;
  font-size: 16px;
  cursor: pointer;
  padding-left: 0;
}
</style>
