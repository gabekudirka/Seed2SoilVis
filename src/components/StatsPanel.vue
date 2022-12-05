/* eslint-disable func-names */
/* eslint-disable */
<template>
  <div>
    <div id="stats-panel" ref="mapElement">
        <TableVis :fleetObj="fleetObj"/>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import TableVis from './TableVis.vue';

export default {
    name: 'StatsPanel',
    components: {
        TableVis
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
            fleet: this.fleetObj.vehicles,
            departments: this.deptsObj.departments,
        };
    },
    computed: {

    },

    methods: {
        
    }
};
</script>

<style>
#stats-panel {
    overflow-y: auto;
}
</style>
