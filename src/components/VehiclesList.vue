/* eslint-disable no-confusing-arrow */
<template>
  <div>
    <ul id="busList">
        <li class="header">
            <!-- <input type="checkbox" v-model="allOn" @change="checkAll()" style="margin:0 0.6em"/> -->
            <div class="row-section-md" @click="sortVehicles('id')">Vehicle</div> 
            <div class="row-section-md" @click="sortVehicles('department')">Department</div>
            <div class="row-section-sm" @click="sortVehicles('utilization_rate')"> Utilization </div>
        </li>
        <li v-for="item in fleet" 
            :key="item.id"
            :class="[item.id == selectedVehicle ? 'selected' : '', 'listItem']"
            @click="selectItem(item.id)"
        > 
            <!-- <input class="row-section-checkbox" type="checkbox" name="check" checked="true" @change="checkOne(item.id)"/> -->
            <div class="row-section-md">{{ item.id }}</div>
            <div class="row-section-md">{{ item.department }}</div>
            <div class="row-section-sm">{{ (item.utilization_rate * 100).toFixed(1) }}%</div>
        </li>
    </ul>
  </div>
</template>

<script>

export default {
    name: 'VehiclesList',
    data() {
        return {
            sortBy: 'department',
            allOn: true,
            onlyConv: false,
            allVehicles: this.fleetObj.vehicles
        };
    },
    props: {
        fleetObj: {
            type: Object,
            required: true,
        },
        tripsObj: {
            type: Object,
            required: true
        },
    },
    computed: {
        fromDate: function () {
            return this.$store.state.fromDate;
        },
        toDate: function () {
            return this.$store.state.toDate;
        },
        selectedVehicle: function () {
            return this.$store.state.selectedVehicle;
        },
        trips: function () {
            return this.tripsObj.trips;
        },
        fleet: function () {
            const fleet = this.allVehicles;
            // Calculate the total idle duration and usage duration for each vehicle in a given period of time
            fleet.forEach(vehicle => {
                const selectedTrips = vehicle.trips.filter(trip => new Date(trip.start_time) >= this.fromDate && new Date(trip.end_time) <= this.toDate);
                const totalDuration = selectedTrips.reduce((accumulator, object) => {
                    return accumulator + object.total_duration;
                }, 0);
                const idleDuration = selectedTrips.reduce((accumulator, object) => {
                    return accumulator + object.idle_duration;
                }, 0);
                vehicle.total_duration = totalDuration;
                vehicle.idle_duration = idleDuration;
                vehicle.num_trips = selectedTrips.length;
            });
            return fleet;
        },
    },
    methods: {
        // When the user selects a vehicle, change the view and update the correspondings state variables
        selectItem: function (vehicleId) {
            const selectedTrips = this.trips.filter(trip => trip.vehicle === vehicleId);
            this.$store.dispatch('changeSelectedTrips', selectedTrips);
            this.$store.dispatch('changeVehicle', vehicleId);
            this.$store.dispatch('changePanelView', true);
        },
        sortVehicles: function (method) {
            let bl = this.fleet;
            if (method === this.sortBy) {
                // just reverse bus list TODO doesnt work
                bl.reverse();
            } else if (method === 'id') {
                bl = this.fleet.sort((a, b) => (a.id > b.id) ? -1 : 1);
            } else if (method === 'department') {
                bl = this.fleet.sort((a, b) => (a.department > b.department) ? 1 : -1);
            } else if (method === 'utilization_rate') {
                bl = this.fleet.sort((a, b) => (a.utilization_rate > b.utilization_rate) ? 1 : -1);
            }
            this.sortBy = method;
            this.fleet = bl;
        },
    }
};

</script>

<style>
.header{
    font-size: smaller;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    border-bottom: 2px solid #cdeceb;
    /* border-top: 2px solid #cdeceb; */
    /* padding: 0.6em; */
    /* padding: 0 0.6em; */
}
.header > div {
    padding: 0 0.6em;
    height: 100%;
    height: 35px;
    display: flex;
    align-items: center;
}
.header > div:hover {
    background-color: #cdeceb;
    text-align: center;
}
.selected {
    color: white;
    background: lightseagreen !important;
}
ul#busList > li:nth-of-type(odd) {
    background-color: white;
}
.listItem{
    padding: 0.6em;
    text-align:center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
}
.listItem .pointer{
    cursor: pointer;
}
.hidden{
    visibility: hidden;
}
.row-section-checkbox{
    width: 5%;
}
.row-section-sm{
    width: 45%;
    text-align: center;
}
.row-section-md{
    width: 55%;
    text-align: center;
}

</style>
