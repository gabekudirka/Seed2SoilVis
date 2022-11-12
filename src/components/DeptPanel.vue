/* eslint-disable */
<template>
    <div class="left-align" style="padding:1em">    
        <div class="row1">
            <div class="left-align flex1 col-3">
                <h4>
                    {{ department.name }} 
                </h4>
                <p> <b> Number of Vehicles: </b> {{ department.num_vehicles }} </p>

            </div>
            <div class="flex1">
                <div id="miles-chart-container" class="chart">
                    <p class="chart-title"> <b> Department Vehicle Usage </b> </p>
                    <PanelChart
                        :chartData="trips"
                        :chartName="'deptDrivingDuration'"
                        :containerWidth="chartSize.width"
                        :containerHeight="chartSize.height"
                    />
                </div>
            </div>
            <div class="flex1">
                <DateSelect />
                <VehicleSubList :fleetObj="fleetObj" :tripsObj="tripsObj"/>
            </div>
        </div>
    </div>
</template>

<script>
import PanelChart from './PanelChart.vue';
import stopsList from '../data/allStops.json';
import DateSelect from './DateSelect.vue';
import VehicleSubList from './VehicleSubList.vue';

export default {
    name: 'BusPanel',
    components: {
        PanelChart,
        DateSelect,
        VehicleSubList,
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
        };
    },
    computed: {
        deptName: function () {
            return this.$store.state.selectedDept;
        },
        department: function () {
            return this.departments.find((dept) => dept.name === this.deptName);
        },
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
        trips: function () {
            return this.$store.state.selectedTrips;
        },
    },
    // watch: {
    //     vehicleId: function () {
    //         this.trips = this.allTrips.filter((trip) => trip.vehicle === this.vehicleId);
    //     },
    // },
    methods: {

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
</style>
