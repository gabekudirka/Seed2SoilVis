// 
/* eslint-disable func-names */
/* eslint-disable */
<template>
  <div id="tableWrapper">
      <table id="dataTable">
                <thead>
                    <tr id="columnHeaders">
                        <th id="vehicleIdCol" class="sortable">Phrase</th>
                        <th id="deptCol" class="sortable">Frequency <svg id="frequencyScale"></svg></th>
                        <th id="utilizationCol" class="sortable">Percentage<svg id="percentScale"></svg></th>
                        <th id="idleTimeCol" class="sortable">Total</th>
                    </tr>
                </thead>
                <tbody id="dataTableBody"></tbody>
            </table>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'TableVis',
    components: {
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
            vizHeight: 22,
            visWidth: 160,
            fleet: this.fleetObj.vehicles,
            // departments: this.deptsObj.departments,
        };
    },
    computed: {
        colorScale: function () {
            return d3.scaleOrdinal();
        }
    },

    methods: {
        rowToCellDataTransform(d) {
            const vehicleId = {
                type: 'text',
                class: 'table-text',
                value: d.id
            };
            const vehicleDept = {
                type: 'text',
                class: 'table-text',
                value: d.department
            };
            // const vehicleUtil = {
            //     type: 'utilVis',
            //     d_percent: d.percent_of_d_speeches,
            //     r_percent: d.percent_of_r_speeches,
            // };
            // const vehicleIdleTime = {
            //     type: 'idleTimeVis',
            //     category: d.category,
            //     frequency: d.frequency
            // };
            
            const dataList = [vehicleId, vehicleDept];
            return dataList;
        },
        drawTable() {
            const rowSelection = d3.select('#dataTableBody')
                .selectAll('tr')
                .data(this.fleet)
                .join('tr');

            const cellSelection = rowSelection.selectAll('td')
                .data(this.rowToCellDataTransform)
                .join('td');

            cellSelection
                .filter(d => d.type === 'text')
                .text(d => d.value);

            // const utilVisSelection = cellSelection.filter(d => d.type === 'utilVis');
            // const idleTimeVisSelection = cellSelection.filter(d => d.type === 'idleTimeVis');

            // const utilSvgSelect = utilVisSelection.selectAll('svg')
            //     .data(d => [d])
            //     .join('svg')
            //     .attr('width', this.visWidth + 8)
            //     .attr('height', this.vizHeight);
            // const idleTimeSvgSelect = idleTimeVisSelection.selectAll('svg')
            //     .data(d => [d])
            //     .join('svg')
            //     .attr('width', this.percentageVisWidth + 8)
            //     .attr('height', this.vizHeight);
            
            // const utilGroupSelect = utilSvgSelect.selectAll('g')
            //     .data(d => [d])
            //     .join('g');
            // const idleTimeGroupSelect = idleTimeSvgSelect.selectAll('g')
            //     .data(d => [d])
            //     .join('g');

            // this.addFrequencyRectangles(utilGroupSelect);
            // this.addPercentageRectangles(idleTimeGroupSelect);
        }
    },
    mounted() {
        this.drawTable();
    },
};
</script>

<style>

</style>
