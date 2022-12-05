/* eslint-disable max-len no-continue */
<template>
    <div>
        <div id="map-panel">
            <!-- <ViewToggle :initShowMap="true"/> -->
            <StatsPanel v-if="!showMapView" :fleetObj="fleetObj" :tripsObj="tripsObj" :deptsObj="deptsObj"/> 
            <MapVis v-if="showMapView"/>
            <DateSelect />
        </div>
    </div>
</template>

<script>
import MapVis from './MapVis.vue';
import ViewToggle from './ViewToggle.vue';
import StatsPanel from './StatsPanel.vue';
import DateSelect from './DateSelect.vue';

export default {
    name: 'MapPanel',
    components: {
        MapVis,
        // ViewToggle,
        StatsPanel,
        DateSelect
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
    computed: {
        showMapView: function () {
            return this.$store.state.showMapView;
        }
    },

};

</script>

<style>
.left-align {
    text-align: left;
    padding:1em;
}
#map-panel {
    overflow-y: auto;
}
</style>
