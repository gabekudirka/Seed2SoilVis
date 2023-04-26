// List the vehicles within a department on the bottom panel when the department view is selected
/* eslint-disable no-confusing-arrow */
<template>
  <div id="vehicles-list-wrapper">
    <ul id="vehicles-list">
        <li class="vehicles-header">
            <input id="vehicles-allon-checkbox" type="checkbox" v-model="allOn" @change="checkAll()" style="margin:0 0.6em"/>
            <div class="vehicle-section-md" @click="sortTrips('id')">Vehicle Id</div> 
            <div class="vehicle-section-sm" @click="sortTrips('total_duration')"># Trips</div>
            <div class="vehicle-section-sm" @click="sortTrips('idle_duration')">Idle Cost</div>
            <div class="vehicle-section-md" @click="sortTrips('total_duration')">Utilization</div>
        </li>   
        <li class='subListItem' v-for="item in vehicles"
            :class="[item.id == selectedVehicle ? 'selected' : '', 'listItem']"
            :key="item.id" 
            @click="selectItem($event, item.id)"
        > 
            <input class="vehicle-section-checkbox" type="checkbox" name="vehicleCheck" checked="true" @change="checkOne(item.id)"/>
            <div class="vehicle-section-md">{{ item.id }}</div>
            <div class="vehicle-section-sm">{{ item.num_trips }}</div>
            <div class="vehicle-section-md">${{ ((item.idle_duration / 60) * 0.2).toFixed(2) }}</div>
            <div class="vehicle-section-md">{{ (item.utilization_rate * 100).toFixed(1) }}%</div>
        </li>
    </ul>
  </div>
</template>

<script>

export default {
    name: 'VehicleSubList',
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
        stateSelectedDept: function () {
            return this.$store.state.selectedDept;
        },
        vehicleIds: function () {
            return this.fleetObj.vehicles.filter(vehicle => vehicle.department === this.stateSelectedDept).map(el => el.id);
        },
        stateSelectedDeptVehicles: function () {
            return this.$store.state.selectedDeptVehicles;
        },
        trips: function () {
            return this.tripsObj.trips.filter(trip => new Date(trip.date) >= this.fromDate && new Date(trip.date) <= this.toDate && this.stateSelectedDeptVehicles.includes(trip.vehicle));
        },
        vehicles: function () {
            const rawVehicles = this.fleetObj.vehicles.filter(vehicle => vehicle.department === this.stateSelectedDept);
            rawVehicles.forEach(vehicle => {
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
            return rawVehicles;
        },
        stateSelectedTrips: function () {
            return this.$store.state.selectedTrips;
        },
    },
    data() {
        return {
            sortBy: 'department',
            allOn: true,
            subsetOn: false,
            onlyConv: false,
            allTrips: this.tripsObj.trips,
        };
    },
    watch: {
        // If a different dept is selected recheck the all on checkbox
        stateSelectedDept: function () {
            this.allOn = true;
        }   
    },
    methods: {
        // When the user selects a vehicle, change the view and update the correspondings state variables
        selectItem: function (event, vehicleId) {
            if (event.target.getAttribute('type') === 'checkbox') {
                return;
            }
            const selectedTrips = this.trips.filter(trip => trip.vehicle === vehicleId);
            this.$store.dispatch('changeSelectedTrips', selectedTrips);
            this.$store.dispatch('changeVehicle', vehicleId);
            this.$store.dispatch('changePanelView', true);
            this.$store.dispatch('changeListView', true);
        },
        // When the all on checkbox is checked reselect all the vehicles and update corresponding state variables
        checkAll: function () {
            document.getElementsByName('vehicleCheck').forEach(checkbox => {
                checkbox.checked = this.allOn;
            });

            if (this.allOn) {
                this.$store.dispatch('changeDeptVehicles', this.vehicleIds);
                this.$store.dispatch('changeSelectedTrips', this.trips);
            } else {
                this.$store.dispatch('changeDeptVehicles', []);
                this.$store.dispatch('changeSelectedTrips', []);
            }
        },
        // Determine if a vehicle is checked or unchecked and add/remove it from the corresponding state variables
        checkOne: function (vehicleId) {
            const checkedVehicles = this.stateSelectedDeptVehicles.filter(vehicle => vehicle !== vehicleId);
            if (this.stateSelectedDeptVehicles.length === checkedVehicles.length) {
                const newVehicles = [...this.stateSelectedDeptVehicles, vehicleId];
                this.$store.dispatch('changeDeptVehicles', newVehicles);
                const vehicleTrips = this.trips.filter(trip => trip.vehicle === vehicleId);
                const newTrips = [...this.stateSelectedTrips, ...vehicleTrips];
                this.$store.dispatch('changeSelectedTrips', newTrips);
            } else {
                this.$store.dispatch('changeDeptVehicles', checkedVehicles);    
                const newTrips = this.stateSelectedTrips.filter(trip => trip.vehicle !== vehicleId);
                this.$store.dispatch('changeSelectedTrips', newTrips);
                this.allOn = false;
            }
            let allChecked = true;
            document.getElementsByName('vehicleCheck').forEach(checkbox => {
                if (!checkbox.checked) {
                    allChecked = false;
                }
            });
            this.allOn = allChecked;
        },
        sortTrips: function (method) {
            let bl = this.fleet;
            if (method === this.sortBy) {
                // just reverse bus list TODO doesnt work
                bl.reverse();
            } else if (method === 'date') {
                bl = this.fleet.sort((a, b) => (Date(a.date) > Date(b.date)) ? -1 : 1);
            } else if (method === 'total_duration') {
                bl = this.fleet.sort((a, b) => (a.total_duration > b.total_duration) ? 1 : -1);
            }
            this.sortBy = method;
            this.fleet = bl;
        },
        // Helper method for displaying duration
        convertDuration(duration) {
            const hours = Math.floor(parseInt(duration, 10) / 60);
            let minutes = parseInt(duration, 10) % 60;
            if (minutes < 10) {
                minutes = '0' + minutes.toString();
            }
            const durationStr = hours.toString() + ':' + minutes;
            return durationStr;
        },
    }
};

</script>

<style>
#vehicles-list-wrapper {
    margin: 10px;
    margin-left: 37%;
    border: solid #c2c2c2 0.5px;
    border-radius: 4px;
    overflow-y: auto;
    height: 340px;
    width: 340px;
}
.vehicles-list {
    border: 1px;
}
.vehicles-header{
    font-size: smaller;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: white;
    background-color: lightseagreen;
    /* border-top: 2px solid #cdeceb; */
    /* padding: 0.6em; */
    /* padding: 0 0.6em; */
}
.vehicles-header > div {
    padding: 0 0.6em;
    height: 100%;
    height: 30px;
    display: flex;
    align-items: center;
    text-align: center;
}
.selected {
    color: white;
    background: lightseagreen !important;
}
ul#vehicles-list > li:nth-of-type(even) {
    background-color: white;
}
.subListItem{
    padding: 0.6em;
    text-align:center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
}
.hidden{
    visibility: hidden;
}
.vehicle-section-checkbox{
    width: 5%;
    align-content: left;
}
.vehicle-section-sm{
    width: 20%;
    text-align: center;
}
.vehicle-section-md{
    width: 26%;
    text-align: center;
}

</style>
