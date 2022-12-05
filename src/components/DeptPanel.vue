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
            </div>
            <div class="flex3">
                <div id="miles-chart-container" class="chart">
                <select class="bootstrap-select chart-select" @change="switchChart($event)">
                    <option value="dept-usage" selected="selected">Total Usage Duration</option>
                    <option value="dept-idle">Idle Time Duration</option>
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
                <p class='list-title'> Vehicles in Department </p>
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
    // watch: {
    //     vehicleId: function () {
    //         this.trips = this.allTrips.filter((trip) => trip.vehicle === this.vehicleId);
    //     },
    // },
    methods: {
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
