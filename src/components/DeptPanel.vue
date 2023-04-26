// Contains code displaying department details on the bottom panel
/* eslint-disable */
<template>
    <div class="left-align" style="padding:1em">    
        <div class="row1">
            <div class="left-align flex1">
                <h3>Department:</h3>
                <h4>
                    {{ department.name }} 
                </h4>
                <p> <b> Number of Vehicles: </b> {{ department.num_vehicles }} </p>
                <br>
                <p> <b> Total Idling Cost: </b> ${{ totalIdlingCost.toFixed(2) }} </p>
                <p> <b> Avg. Utilization Rate: </b> {{ (department.avg_utilization_rate * 100).toFixed(1) }}% </p>
                <p> <b> Avg. Days Driven Utilization: </b> {{ (department.avg_days_utilization * 100).toFixed(1) }}% </p>
                <p> <b> Avg. Duration Utilization: </b> {{ (department.avg_duration_utilization * 100).toFixed(1) }}% </p>
                <p> <b> Avg. Distance Utilization: </b> {{ (department.avg_distance_utilization * 100).toFixed(1) }}% </p>
            </div>
            <div class="flex2">
                <div id="miles-chart-container" class="chart">
                <select class="bootstrap-select chart-select" @change="switchChart($event)">
                    <option value="dept-usage" selected="selected">Total Usage Duration</option>
                    <option value="dept-idle">Idling Cost</option>
                    <option value="dept-driving">Driving Duration</option>
                    <option value="dept-distance">Distance Traveled</option>
                </select>
                    <DeptPanelChart
                        :chartData="timeSelectedTrips"
                        :chartType="chartType"
                        :chartDataType="chartDataType"
                        :containerWidth="chartSize.width"
                        :containerHeight="chartSize.height"
                    />
                </div>
            </div>
            <div class="flex2">
                <!-- <DateSelect /> -->
                <div id='vehicles-list-title'>
                    <p class='list-title vehicles-title'> Vehicles in Department </p>
                </div>
                <VehicleSubList :fleetObj="fleetObj" :tripsObj="tripsObj"/>
            </div>
        </div>
    </div>
</template>

<script>
import DeptPanelChart from './DeptPanelChart.vue';
import VehicleSubList from './VehicleSubList.vue';

export default {
    name: 'DeptPanel',
    components: {
        DeptPanelChart,
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
                height: 350,
                width: 610
            },
            fleet: this.fleetObj.vehicles,
            departments: this.deptsObj.departments,
            chartType: 'day',
            chartDataType: 'total_duration'
        };
    },
    computed: {
        deptName: function () {
            return this.$store.state.selectedDept;
        },
        department: function () {
            return this.departments.find((dept) => dept.name === this.deptName);
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
        // Get all the trips in the selected time span
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
        // accumilate the total idling cost of all vehicles in the department
        totalIdlingCost: function () {
            const totalCost = this.timeSelectedTrips.reduce((a, b) => {
                return a + b.idle_duration;
            }, 0);
            return totalCost;
        },
        // Update the title of the chart based on the data being displayed in the chart
        chartTitle: function () {
            if (this.chartDataType === 'total_duration') {
                return 'Total Usage Duration of Department Vehicles';
            } else if (this.chartDataType === 'idle_duration') {
                return 'Idle Duration of Department Vehicles';
            } else if (this.chartDataType === 'distance') {
                return 'Distance Traveled by Department Vehicles';
            } else if (this.chartDataType === 'driving_duration') {
                return 'Driving Duration of Department Vehicles';
            } else {
                return 'Total Usage Duration of Department Vehicles';
            }
        }
    },
    methods: {
        // This method changes which chart is shown based on what the user has selected from the dropdown
        switchChart(event) {
            if (event.target.value === 'dept-usage') {
                this.chartDataType = 'total_duration';
            } else if (event.target.value === 'dept-idle') {
                this.chartDataType = 'idle_duration';
            } else if (event.target.value === 'dept-distance') {
                this.chartDataType = 'distance';
            } else if (event.target.value === 'dept-driving') {
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
.flex3{
    flex:3;
}
#vehicles-list-title{
   padding-left: 33%
}
p{
    margin: 0.2em !important;
}
.chart{
    max-width:31vw;
}
</style>
