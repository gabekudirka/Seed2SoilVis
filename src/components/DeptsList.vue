/* eslint-disable no-confusing-arrow */
<template>
  <div>
    <ul id="deptsList">
        <li class="header">
            <!-- <input type="checkbox" v-model="allOn" @change="checkAll()" style="margin:0 0.6em"/> -->
            <div class="row-section-sm" @click="sortDepts('name')">Department</div> 
            <div class="row-section-md" @click="sortDepts('num_vehicles')">Num Vehicles</div>
        </li>
        <li v-for="item in departments" 
            :key="item.name"
            :class="[item.name == selectedDept ? 'selected' : '', 'listItem']"
            @click="selectItem(item.name)"
        > 
            <!-- <input class="row-section-checkbox" type="checkbox" name="check" checked="true" @change="checkOne(item.id)"/> -->
            <div class="row-section-sm">{{ item.name }}</div>
            <div class="row-section-md">{{ item.num_vehicles }}</div>
        </li>
    </ul>
  </div>
</template>

<script>

export default {
    name: 'DeptsList',
    data() {
        return {
            fleet: this.fleetObj.vehicles,
            departments: this.deptsObj.departments,
            allTrips: this.tripsObj.trips
        };
    },
    props: {
        deptsObj: {
            type: Object,
            required: true
        },
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
        selectedDept: function () {
            return this.$store.state.selectedDept;
        },
    },
    methods: {
        selectItem: function (deptName) {
            this.$store.dispatch('changeDept', deptName);
            const deptVehicles = this.fleet.filter(vehicle => vehicle.department === deptName).map(vehicle => vehicle.id);
            const selectedTrips = this.allTrips.filter(trip => deptVehicles.includes(trip.vehicle));
            this.$store.dispatch('changeSelectedTrips', selectedTrips);
            this.$store.dispatch('changePanelView', false);
        },
        sortDepts: function (method) {
            let bl = this.departments;
            if (method === this.sortBy) {
                // just reverse bus list TODO doesnt work
                bl.reverse();
            } else if (method === 'name') {
                bl = this.departments.sort((a, b) => (a.name > b.name) ? -1 : 1);
            } else if (method === 'num_vehicles') {
                bl = this.departments.sort((a, b) => (a.num_vehicles > b.num_vehicles) ? 1 : -1);
            }
            this.sortBy = method;
            this.departments = bl;
        },
    }
};

</script>

<style>
.selected {
    color: white;
    background: lightseagreen !important;
}
ul#deptsList > li:nth-of-type(odd) {
    background-color: white;
}
.listItem{
    padding: 0.6em;
    text-align:left;
}
.listItem:hover{
    background-color: #cdeceb !important;
}

</style>
