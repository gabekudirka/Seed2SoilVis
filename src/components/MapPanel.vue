/* eslint-disable max-len no-continue */
<template>
    <div>
        <div class="map">
            <BusMap/> 
        </div>
    </div>
</template>

<script>
import BusMap from './BusMap.vue';

export default {
    name: 'MapPanel',
    components: {
        BusMap,
    },
    computed: {
        time: function () {
            return this.$store.state.time;
        },
        // returns array of {busID: ID, coordinates: [lat,long]}
        busLocations: function () { 
            return this.$store.state.busLocations;
        }
    },

};

</script>

<style>
.left-align {
    text-align: left;
    padding:1em;
}
</style>
