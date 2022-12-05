<template>
    <div id="vis">
        <div class="date-select-wrapper"> 
            <label for="start-date" class="input-label label">From Date:</label>
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
            <label for="end-date" class="input-label label">To Date:</label>
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
    watch: {
        fromDate() {
            this.$store.dispatch('changeFromDate', this.fromDate);
        },
        toDate() {
            this.$store.dispatch('changeToDate', this.toDate);
        },
    },
};
</script>

<style>
    #vis{
        /* padding-top: 0px;
        display: flex;
        margin-left: 19%; */
        position: absolute;
        z-index: 11;
        left: 40%;
        top: 0%;
        background-color: white;
        border-radius: 5px;
        height: 65px;
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
        width: 140px;
    }
    .label {
        font-weight: bold;
        font-size: 14px;
    }
</style>
