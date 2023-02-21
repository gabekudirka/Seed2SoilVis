<template>
  <div class="toggle-switch" id="map-view-toggle">
    <button
        class="button toggle"
        @click="toggle"
        :class="[!showMapView ? 'active' : '']" 
    >Stats</button>
    <button
        class="button toggle"
        @click="toggle"
        :class="[showMapView ? 'active' : '']"
    >Map</button>
    </div>
</template>

<script>

export default {
    name: 'ViewToggle',
    props: {
        initShowMap: {
            type: Boolean,
            default: true
        }
    },
    data() {
        return {
            showMapView: this.initShowMap,
        };
    },
    computed: {
        showMapViewState: function () {
            return this.$store.state.showMapView;
        },
    },
    watch: {
        showMapViewState: function () {
            this.changeToggle();
        }
    },
    methods: {
        // change the map view when the toggle is clicked
       toggle() {
            this.$store.dispatch('changeMainView', !this.showMapView);
        },
        changeToggle() {
            this.showMapView = !this.showMapView;
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
#map-view-toggle {
    position: absolute;
    z-index: 10;
    top: 90%;
}

/* div.container {
  max-width: 80%;
} */

</style>
