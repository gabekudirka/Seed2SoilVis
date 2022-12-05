/* eslint-disable no-confusing-arrow */
<template>
  <div id="trips-list-wrapper">
    <ul id="trips-list">
        <li class="trips-header">
            <input id="trips-allon-checkbox" type="checkbox" v-model="allOn" @change="checkAll()" style="margin:0 0.6em"/>
            <div class="trip-section-sm" @click="sortTrips('date')">Date</div> 
            <div class="trip-section-md" @click="sortTrips('total_duration')">Trip Duration</div>
            <div class="trip-section-md" @click="sortTrips('idle_duration')">Idle Duration</div>
        </li>
        <li class='tripListItem' v-for="item in vehicleTrips" 
            :key="item.id"
        > 
            <input class="trip-section-checkbox" type="checkbox" name="tripCheck" checked="true" @change="checkOne(item.id)"/>
            <div class="trip-section-sm">{{ (new Date(item.date)).getMonth() }}/{{ (new Date(item.date)).getDate() }}/{{ (new Date(item.date)).getFullYear() }}</div>
            <div class="trip-section-md">{{ convertDuration(item.total_duration) }} </div>
            <div class="trip-section-md">{{ convertDuration(item.idle_duration) }}</div>
        </li>
    </ul>
  </div>
</template>

<script>

export default {
    name: 'TripsList',
    props: {
        tripsObj: {
            type: Object,
            required: true,
        },
    },
    computed: {
        fromDate: function () {
            return this.$store.state.fromDate;
        },
        toDate: function () {
            return this.$store.state.toDate;
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
        stateSelectedVehicle: function () {
            this.allOn = true;
        }
    },
    methods: {
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
        convertDuration(duration) {
            const hours = Math.floor(parseInt(duration, 10) / 60);
            let minutes = parseInt(duration, 10) % 60;
            if (minutes < 10) {
                minutes = '0' + minutes.toString();
            }
            const durationStr = hours.toString() + ':' + minutes;
            return durationStr;
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
            let bl = this.vehicleTrips;
            if (method === this.sortBy) {
                // just reverse bus list TODO doesnt work
                bl.reverse();
            } else if (method === 'date') {
                bl = this.vehicleTrips.sort((a, b) => (Date(a.date) > Date(b.date)) ? -1 : 1);
            } else if (method === 'total_duration') {
                bl = this.vehicleTrips.sort((a, b) => (a.total_duration > b.total_duration) ? 1 : -1);
            } else if (method === 'idle_duration') {
                bl = this.vehicleTrips.sort((a, b) => (a.idle_duration > b.idle_duration) ? 1 : -1);
            }
            this.sortBy = method;
            this.vehicleTrips = bl;
        },
    
    }
};

</script>

<style>
#trips-list-wrapper {
    margin: 10px;
    /* margin-left: 0%; */
    border: solid #c2c2c2 0.5px;
    border-radius: 4px;
    overflow-y: auto;
    height: 340px;
    width: 340px;
}
#trips-list {
    border-radius: 5px;
}
.trips-header{
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
.trips-header > div {
    padding: 0 0.6em;
    height: 100%;
    height: 30px;
    display: flex;
    align-items: center;
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
.trip-section-checkbox{
    width: 7%;
    align-content: left;
}
.trip-section-sm{
    width: 25%;
    text-align: center;
}
.trip-section-md{
    width: 34%;
    text-align: center;
}

</style>
