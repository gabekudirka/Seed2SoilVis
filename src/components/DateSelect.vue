<template>
    <div id="vis">
        <div class="date-select-wrapper"> 
            <label for="start-date" class="input-label label">Show Trips From:</label>
            <Datepicker
                id="start-date" 
                class="date-picker input-label"
                type="text"
                v-model="fromDate"
                :upperLimit="toDate"
                :lowerLimit="minDate"
                :typeable="true"/>
        </div>
        <div class="date-select-wrapper"> 
            <label for="end-date" class="input-label label">Show Trips To:</label>
            <Datepicker
                id="end-date" 
                class="date-picker input-label"
                type="text"
                v-model="toDate"
                :upperLimit="maxDate"
                :lowerLimit="fromDate"
                :typeable="true"/>
        </div>
    </div>
</template>

<script>
import Datepicker from 'vue3-datepicker';
import { ref } from 'vue';

export default {
    name: 'DateSelect',
    components: {
        Datepicker
    },
    data() {
        return {
            fromDate: this.$store.state.fromDate,
            toDate: this.$store.state.toDate,
            minDate: this.$store.state.minDate,
            maxDate: this.$store.state.maxDate,
        };
    },
    // setup() {
    //   const fromDate = this.$store.state.fromDate;
    //   const toDate = this.$store.state.toDate;
    //   const minDate = this.$store.state.minDate;
    //   const maxDate = this.$store.state.maxDate;
 
    //   return {
    //      fromDate,
    //      toDate,
    //      minDate,
    //      maxDate,
    //   };
    // },
    computed: {

    },
    watch: {
        fromDate() {
            this.$store.dispatch('changeFromDate', this.fromDate);
        },
        toDate() {
            this.$store.dispatch('changeToDate', this.toDate);
        },
    },
    methods: {
    },
    mounted() {

    }
};
</script>

<style>
    #vis{
        padding-top: 0px;
        display: flex;
        margin-left: 19%
    }
    .input-label {
        display: block;
        margin-top: 0px;
        margin-bottom: 0px;
    }
    .date-select-wrapper {
        float: left;
        margin-left: 10px;
        margin-right: 10px;
    }
    .date-picker {
        width: 120px;
    }
    .label {
        font-weight: bold;
        font-size: 12px;
    }
</style>
