<template>
  <div class="toggle-switch">
    <button
        class="button toggle"
        @click="toggle"
        :class="[!showVehicleList ? 'active' : '']" 
    >Departments</button>
    <button
        class="button toggle"
        @click="toggle"
        :class="[showVehicleList ? 'active' : '']"
    >Vehicles</button>
    </div>
</template>

<script>

export default {
    name: 'ToggleSwitch',
    props: {
        initShowVehicleList: {
            type: Boolean,
            default: true
        }
    },
    data() {
        return {
            showVehicleList: this.initShowVehicleList,
        };
    },
    computed: {
        showVehicleListState: function () {
            return this.$store.state.showVehicleList;
        }
    },
    watch: {
        showVehicleListState: function () {
            this.changeToggle();
        }
    },
    methods: {
       toggle() {
            this.$store.dispatch('changeListView', !this.showVehicleList);
        },
        changeToggle() {
            this.showVehicleList = !this.showVehicleList;
        }
    },
};

</script>

<style>
.toggle-switch{
    margin:1em;
}
.toggle {
    padding: 2px 6px ;
}
.toggle-switch > .toggle:first-of-type {
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
}
.toggle-switch > .toggle:last-of-type {
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}
button{
    border: 1.5px solid lightseagreen;
    color: lightseagreen;
}
.active{
    background-color: lightseagreen;
    color: white;
}

/* div.container {
  max-width: 80%;
} */

</style>
