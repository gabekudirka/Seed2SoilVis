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
                <p> <b> Trips Taken: </b> {{ vehicle.num_trips }} </p>
            </div>
            <div class="flex2">
                <div id="miles-chart-container" class="chart">
                <select class="bootstrap-select chart-select" @change="switchChart($event)">
                    <option value="vehicle-usage" selected="selected">Total Usage Duration</option>
                    <option value="vehicle-idle">Idle Time Duration</option>
                    <option value="vehicle-driving">Driving Duration</option>
                    <option value="vehicle-distance">Distance Traveled</option>
                </select>
                    <VehiclePanelChart
                        :chartData="timeSelectedTrips"
                        :chartDataType="chartDataType"
                        :containerWidth="chartSize.width"
                        :containerHeight="chartSize.height"
                    />
                </div>
            </div>
            <div class="flex1">
                <!-- <DateSelect /> -->
                <p class='list-title'> Trips Taken by Vehicle </p>
                <TripList :tripsObj="tripsObj"/>
            </div>
        </div>
    </div>
</template>

<script>
import VehiclePanelChart from './VehiclePanelChart.vue';
import DateSelect from './DateSelect.vue';
import TripList from './TripList.vue';

export default {
    name: 'VehiclePanel',
    components: {
        VehiclePanelChart,
        // DateSelect,
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
                height: 350,
                width: 575
            },
            fleet: this.fleetObj.vehicles,
            departments: this.deptsObj.departments,
            allTrips: this.tripsObj.trips,
            chartDataType: 'total_duration'
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
        timeSelectedTrips: function () {
            return this.stateSelectedTrips.filter(trip => new Date(trip.date) >= this.fromDate && new Date(trip.date) <= this.toDate);
        },
        chartTitle: function () {
            if (this.chartDataType === 'total_duration') {
                return 'Total Usage Duration';
            } else if (this.chartDataType === 'idle_duration') {
                return 'Idle Duration';
            } else if (this.chartDataType === 'distance') {
                return 'Distance Traveled';
            } else if (this.chartDataType === 'driving_duration') {
                return 'Driving Duration';
            } else {
                return 'Total Usage Duration';
            }
        }
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
            const selectedTrips = this.allTrips.filter(trip => new Date(trip.date) >= this.fromDate && new Date(trip.date) <= this.toDate && deptVehicles.includes(trip.vehicle));
            this.$store.dispatch('changeDeptVehicles', deptVehicles);
            this.$store.dispatch('changeSelectedTrips', selectedTrips);
            this.$store.dispatch('changePanelView', false);
            this.$store.dispatch('changeListView', false);
        },
        switchChart(event) {
            if (event.target.value === 'vehicle-usage') {
                this.chartDataType = 'total_duration';
            } else if (event.target.value === 'vehicle-idle') {
                this.chartDataType = 'idle_duration';
            } else if (event.target.value === 'vehicle-distance') {
                this.chartDataType = 'distance';
            } else if (event.target.value === 'vehicle-driving') {
                this.chartDataType = 'driving_duration';
            }
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
.flex2{
    flex:2;
}
.chart-select{
    text-align: center;
    font-size: 16px;
    font-weight: bold;
    display: block;
    margin: 0 auto;
    margin-top: 0px;
    margin-bottom: 5px;
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
.list-title {
    font-weight: bold;
    font-size: 16px;
    text-align: center;
}
</style>
