/* eslint-disable no-confusing-arrow */
<template>
  <div id="trips-list-wrapper">
    <ul id="trips-list">
        <li class="trips-header">
            <div > 
                <input id="trips-allon-checkbox" type="checkbox" v-model="allOn" @change="checkAll()" style="margin:0 0.6em"/>
            </div>
            <div class="row-section-sm" @click="sortTrips('id')">Vehicle Id</div> 
            <div class="row-section-md" @click="sortTrips('year')">Year</div>
        </li>
        <li class='tripListItem' v-for="item in vehicles" 
            :class="[item.id == selectedVehicle ? 'selected' : '', 'listItem']"
            :key="item.id"
            @click="selectItem(item.id)"
        > 
            <input class="row-section-checkbox" type="checkbox" name="tripCheck" checked="true" @change="checkOne(item.id)"/>
            <div class="row-section-sm">{{ item.id }}</div>
            <div class="row-section-md">{{ item.year }}</div>
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
        vehicles: function () {
            return this.fleetObj.vehicles.filter(vehicle => vehicle.department === this.stateSelectedDept);
        },
        trips: function () {
            return this.tripsObj.trips;
        },
        showVehiclesState: function () {
            return this.$store.state.showVehicles;
        },
        vehicleTrips: function () {
            return this.tripsObj.trips.filter(trip => trip.vehicle === this.stateSelectedVehicle && new Date(trip.date) >= this.fromDate && new Date(trip.date) <= this.toDate);
        },
        stateSelectedTrips: function () {
            return this.$store.state.selectedTrips;
        },
        stateSelectedVehicle: function () {
            return this.$store.state.selectedVehicle;
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
        stateSelectedDept: function () {
            this.allOn = true;
        }
    },
    methods: {
        selectItem: function (vehicleId) {
            const selectedTrips = this.trips.filter(trip => trip.vehicle === vehicleId);
            this.$store.dispatch('changeSelectedTrips', selectedTrips);
            this.$store.dispatch('changeVehicle', vehicleId);
            this.$store.dispatch('changePanelView', !this.showVehiclesState);
        },
        checkAll: function () {
            document.getElementsByName('tripCheck').forEach(checkbox => {
                checkbox.checked = this.allOn;
            });

            if (this.allOn) {
                this.$store.dispatch('changeSelectedTrips', this.vehicleTrips);
            } else {
                this.$store.dispatch('changeSelectedTrips', []);
            }
        },
        checkOne: function (tripId) {
            const checkedTrips = this.stateSelectedTrips.filter(trip => trip.id !== tripId);
            const trip = this.vehicleTrips.find(el => el.id === tripId);
            if (this.stateSelectedTrips.length === checkedTrips.length) {
                const newTrips = [...this.stateSelectedTrips, trip];
                this.$store.dispatch('changeSelectedTrips', newTrips);
            } else {
                this.$store.dispatch('changeSelectedTrips', checkedTrips);
                this.allOn = false;
            }
            let allChecked = true;
            document.getElementsByName('tripCheck').forEach(checkbox => {
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
    
    }
};

</script>

<style>
#trips-list-wrapper {
    margin: 10px;
    margin-left: 18%;
    width: 300px;
    height: 280px;
    border: solid black 0.5px;
    border-radius: 2px;
    overflow-y: auto;
}
.trips-list {
    border: 1px;
}
.trips-header{
    font-size: smaller;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    background-color: #bfbfbf;
    /* border-top: 2px solid #cdeceb; */
    /* padding: 0.6em; */
    /* padding: 0 0.6em; */
}
.trips-header > div {
    padding: 0 0.6em;
    height: 100%;
    height: 30px;
    display: flex;
    align-items: center;
}
.trips-header > div:hover {
    background-color: #cdeceb;
}
.selected {
    color: white;
    background: lightseagreen !important;
}
ul#trips-list > li:nth-of-type(even) {
    background-color: white;
}
.tripListItem{
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
.row-section-checkbox{
    width: 5%;
    align-content: left;
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
