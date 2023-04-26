// Container for both the department and vehicles list on the left panel
<template>
  <div>
    <ListToggle :initShowVehicleList="showVehicleList" /> 
    <div class="lists">
        <VehiclesList v-if="showVehicleList" :fleetObj="fleetObj" :tripsObj="tripsObj"/>
        <DeptsList v-if="!showVehicleList" :deptsObj="deptsObj" :fleetObj="fleetObj" :tripsObj="tripsObj"/>
    </div>
  </div>
</template>

<script>
import ListToggle from './ListToggle.vue';
import DeptsList from './DeptsList.vue';
import VehiclesList from './VehiclesList.vue';

export default {
    name: 'ListContainer',
    components: {
        ListToggle,
        DeptsList,
        VehiclesList
    },
    props: {
        fleetObj: {
            type: Object,
            required: true
        },
        tripsObj: {
            type: Object,
            required: true
        },
        deptsObj: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            modalVisible: false
        };
    },
    computed: {
        showVehicleList: function () {
            return this.$store.state.showVehicleList;
        }
    },
};

</script>

<style>
.helpBtn{
    font-size: x-large;
    color: #94cecb;
    position:fixed;
    top: 5px;
    left: 5px;
}
.helpBtn:hover{
    cursor: pointer;
}
#routeList{
    overflow-x: hidden;
    overflow-y: auto;
}
/* div.container {
  max-width: 80%;
} */

</style>
