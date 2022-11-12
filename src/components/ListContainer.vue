<template>
  <div>
    <i 
        class="fas fa-question-circle helpBtn"  
        @click="showModal"
        title="Help"
    ></i>
    <HelpModal v-show="modalVisible" @close="closeModal"/>
    <ToggleSwitch :initShowVehicleList="showVehicleList" /> 
    <div class="lists">
        <VehiclesList v-if="showVehicleList" :fleetObj="fleetObj" :tripsObj="tripsObj"/>
        <DeptsList v-if="!showVehicleList" :deptsObj="deptsObj" :fleetObj="fleetObj" :tripsObj="tripsObj"/>
    </div>
  </div>
</template>

<script>
import ToggleSwitch from './ToggleSwitch.vue';
import DeptsList from './DeptsList.vue';
import VehiclesList from './VehiclesList.vue';
import HelpModal from './HelpModal.vue';

export default {
    name: 'ListContainer',
    components: {
        ToggleSwitch,
        DeptsList,
        VehiclesList,
        HelpModal
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
    methods: {
        showModal() {
            this.modalVisible = true;
        },
        closeModal() {
            this.modalVisible = false;
        },
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
