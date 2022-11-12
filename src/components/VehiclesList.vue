/* eslint-disable no-confusing-arrow */
<template>
  <div>
    <ul id="busList">
        <li class="header">
            <!-- <input type="checkbox" v-model="allOn" @change="checkAll()" style="margin:0 0.6em"/> -->
            <div class="row-section-sm" @click="sortVehicles('id')">Vehicle</div> 
            <div class="row-section-md" @click="sortVehicles('department')">Department</div>
        </li>
        <li v-for="item in fleet" 
            :key="item.id"
            :class="[item.id == selectedVehicle ? 'selected' : '', 'listItem']"
            @click="selectItem(item.id)"
        > 
            <!-- <input class="row-section-checkbox" type="checkbox" name="check" checked="true" @change="checkOne(item.id)"/> -->
            <div class="row-section-sm">{{ item.id }}</div>
            <div class="row-section-md">{{ item.department }}</div>
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
            fleet: this.fleetObj.vehicles
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
        selectedVehicle: function () {
            return this.$store.state.selectedVehicle;
        },
        trips: function () {
            return this.tripsObj.trips;
        },
    },
    watch: {
    },
    methods: {
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
