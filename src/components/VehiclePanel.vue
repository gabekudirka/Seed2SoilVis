// Displays vehicle details in the bottom panel. Also a container for the vehicle panel chart
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
                <br>
                <p> <b> Idling Cost: </b> ${{ totalIdlingCost.toFixed(2) }} </p>
                <p> <b> Utilization Rate: </b> {{ (vehicle.utilization_rate * 100).toFixed(1) }}% </p>
                <p> <b> Days Driven' Utilization: </b> {{ (vehicle.days_utilization * 100).toFixed(1) }}% </p>
                <p> <b> Duration Utilization: </b> {{ (vehicle.duration_utilization * 100).toFixed(1) }}% </p>
                <p> <b> Distance Utilization: </b> {{ (vehicle.distance_utilization * 100).toFixed(1) }}% </p>
            </div>
            <div class="flex2">
                <div id="miles-chart-container" class="chart">
                    <div id='vehicle-chart-tooltip-container'>
                        <select class="bootstrap-select chart-select" @change="switchChart($event)">
                            <option value="vehicle-usage" selected="selected">Total Usage Duration</option>
                            <option value="vehicle-idle">Idling Cost</option>
                            <option value="vehicle-driving">Driving Duration</option>
                            <option value="vehicle-distance">Distance Traveled</option>
                        </select>
                    </div>
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
import TripList from './TripList.vue';

export default {
    name: 'VehiclePanel',
    components: {
        VehiclePanelChart,
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
        // Get all trips within the selected date range
        timeSelectedTrips: function () {
            const tripsData = this.stateSelectedTrips.filter(trip => new Date(trip.date) >= this.fromDate && new Date(trip.date) <= this.toDate);
            const costData = [];
            if (tripsData) {
                tripsData.forEach(trip => {
                    const costTrip = { ...trip };
                    const cost = Number(((trip.idle_duration / 60) * 0.2).toFixed(2));
                    costTrip.idle_duration = cost;
                    costData.push(costTrip);
                });
            }
            
            return costData;
        },
        // Accumulate idle cost of all trips taken by the vehicle
        totalIdlingCost: function () {
            const totalCost = this.timeSelectedTrips.reduce((a, b) => {
                return a + b.idle_duration;
            }, 0);
            return totalCost;
        },
        // Update the chart title depending on the data being displayed
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

    methods: {
        // When you select the vehicles department name, switch to the department view and change corresponding state variables
        showDept(deptName) {
            this.$store.dispatch('changeDept', deptName);
            const deptVehicles = this.fleet.filter(vehicle => vehicle.department === deptName).map(vehicle => vehicle.id);
            const selectedTrips = this.allTrips.filter(trip => new Date(trip.date) >= this.fromDate && new Date(trip.date) <= this.toDate && deptVehicles.includes(trip.vehicle));
            this.$store.dispatch('changeDeptVehicles', deptVehicles);
            this.$store.dispatch('changeSelectedTrips', selectedTrips);
            this.$store.dispatch('changePanelView', false);
            this.$store.dispatch('changeListView', false);
        },
        // Switch the chart when the user selects a different one from the dropdown
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
#vehicle-chart-tooltip-container {
    padding-left: 30px;
}
</style>
