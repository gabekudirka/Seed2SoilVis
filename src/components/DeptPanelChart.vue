<template>
    <div id='tooltip'>
    </div>
    <svg id="dept-svg">
        <g v-bind:id="chartName" transform="translate(27, 5)"> </g>
    </svg>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'DeptPanelChart',
    props: {
        chartData: {
            required: true,
            type: Array,
        },
        chartDataType: {
            required: true,
            type: String,
        },
        containerWidth: {
            default: 375,
            type: Number,
        },
        containerHeight: {
            default: 210,
            type: Number,
        }
    },
    data() {
        return {
            margin: { 
                top: 15, 
                right: 25, 
                bottom: 40, 
                left: 25 
            },
            chartName: 'dept-chart',
            colorScale: null,
        };
    },
    computed: {
        width: function () {
            return this.containerWidth - this.margin.left - this.margin.right;
        },
        height: function () {
            return this.containerHeight - this.margin.top - this.margin.bottom;
        },
        fromDate: function () {
          return this.$store.state.fromDate;
        },
        toDate: function () {
          return this.$store.state.toDate;
        },
        viewBox: function () {
            return `0 0 ${this.containerWidth} ${this.containerHeight}`;
        },
        selectedVehicles: function () {
          return this.$store.state.selectedDeptVehicles;
        },
        stateSelectedDeptVehicles: function () {
            return this.$store.state.selectedDeptVehicles;
        },
        yLabel: function () {
            if (this.chartDataType === 'total_duration') {
                return 'Total Usage Duration (minutes)';
            } else if (this.chartDataType === 'idle_duration') {
                return 'Idle Cost ($)';
            } else if (this.chartDataType === 'distance') {
                return 'Distance Traveled (miles)';
            } else if (this.chartDataType === 'driving_duration') {
                return 'Driving Duration (minutes)';
            } else {
                return 'Total Usage Duration (minutes)';
            }
        },
    },
    watch: {
        // When the chart data changes, update the chart
        chartData: function () {
            this.colorScale = d3.scaleOrdinal()
                .domain(this.selectedVehicles)
                .range(d3.schemeDark2);
            this.clearChart();
            this.renderDeptChart();
        },
        chartDataType: function () {
            this.clearChart();
            this.renderDeptChart();    
        },
    },
    methods: {
        // This method uses d3 to create a stacked bar chart for the entire department data
        renderDeptChart() {
            const ref = this; 
            
            // This is initial data processing for the visualization
            const dates = this.getDatesInRange(this.fromDate, this.toDate);
            const testDate = new Date(this.fromDate.getTime());
            const dateData = dates.map(el => {
                const dataPoint = { date: el };
                ref.selectedVehicles.forEach(vehicle => {
                    dataPoint[vehicle] = 0;
                });
                const tripsOnDate = this.chartData.filter(pt => {
                    const tripDate = new Date(pt.date);
                    const dateStr = (tripDate.getMonth() + 1) + '/' + tripDate.getDate();
                    return dateStr === el;
                });
                let durationSum = 0;
                tripsOnDate.forEach(trip => {
                    dataPoint[trip.vehicle] = trip[ref.chartDataType];
                    durationSum += trip[ref.chartDataType];
                });
                dataPoint.sum = durationSum;
                return dataPoint; 
            });

            // Creates a stack generator for the data
            const stackGen = d3.stack()
                .keys(this.selectedVehicles)
                .order(d3.stackOrderNone)
                .offset(d3.stackOffsetNone);

            const stack = stackGen(dateData);
            const xScale = d3.scaleBand()
                .domain(dates)
                .range([this.margin.left, this.width]);
                // .padding(0.1);

            const max = dateData.length > 0 ? d3.max(dateData, d => d.sum) : 500;
            const yScale = d3.scaleLinear()
                .domain([0, max])
                .range([this.height + this.margin.top, 0])
                .nice();

            const ticks = Math.floor(dates.length / 10);
            const xAxis = d3.axisBottom(xScale)
                        .tickValues(xScale.domain().filter((d, i) => { return !(i % ticks); }));
                        // .scale(xScale);
            const yAxis = d3.axisLeft()
                        .scale(yScale)
                        .ticks(8); 

            // Creates the tooltip for the barchart
            const tooltip = d3.select('#tooltip')
                .style('opacity', 0)
                .attr('class', 'tooltip')
                .style('background-color', 'white')
                .style('border', 'solid')
                .style('border-width', '1px')
                .style('border-radius', '5px')
                .style('padding', '10px');

            const mouseover = function (event, d) {
                const vehicle = d3.select(this.parentNode).datum().key;
                const vehicleDuration = d.data[vehicle];
                tooltip
                        .html('Vehicle: ' + vehicle + '<br>Vehicle total: ' + vehicleDuration)
                        .style('opacity', 1);      
            };
            const mousemove = function (event, d) {
                tooltip
                    .style('left', event.layerX + 15 + 'px')
                    .style('top', event.layerY + 'px');
            };
            const mouseleave = function (event, d) {
                tooltip
                    .style('opacity', 0);
            };

            // Creates the stacked barchart using the processed data
            const g = d3.select(`#${this.chartName}`);
            g
                .selectAll('g')
                .data(stack)
                .join('g')
                .attr('fill', d => this.colorScale(d.key))
                .selectAll('rect')
                .data(d => d)
                .join('rect')
                .attr('x', d => xScale(d.data.date))
                .attr('y', ([y1, y2]) => Math.min(yScale(y1), yScale(y2)))
                .attr('height', ([y1, y2]) => Math.abs(yScale(y1) - yScale(y2)))
                .attr('width', xScale.bandwidth() - 5)
                .on('mouseover', mouseover)
                .on('mousemove', mousemove)
                .on('mouseleave', mouseleave);
                        
            g.append('g')
                .call(xAxis)
                .style('transform', `translateY(${this.containerHeight - this.margin.bottom}px)`);
            g.append('g')
                .call(yAxis)
                .attr('transform', `translate(${this.margin.left}, 0)`);

            g.append('text')
                .text(this.yLabel)
                .classed('y-axis-label', true)
                .attr('text-anchor', 'end')
                .attr('transform', 'rotate(-90) translate(-70, -15)')
                .style('font-size', '15px');

            const legend = g.append('g');
            legend
                .selectAll('circle')
                .data(this.selectedVehicles)
                .join('circle')
                .attr('cx', 575)
                .attr('cy', (d, i) => 5 + i * 25)
                .attr('r', 8)
                .style('fill', d => this.colorScale(d));
            legend
                .selectAll('text')
                .data(this.selectedVehicles)
                .join('text')
                .attr('x', 592)
                .attr('y', (d, i) => 6 + i * 25)
                .style('fill', d => this.colorScale(d))
                .text(d => d)
                .attr('text-anchor', 'left')
                .style('alignment-baseline', 'middle')
                .style('font-size', 12);
        },
        // renderByVehicleChart() {
        //     const ref = this;
        //     if (this.chartData.length === 0) {
        //         return;
        //     }

        //     const xScale = d3.scaleBand()
        //         .domain(this.selectedVehicles)
        //         .range([this.width, this.margin.left])
        //         .padding(0.3);

        //     const max = this.chartData.length > 0 ? d3.max(this.chartData, d => d[ref.chartDataType]) : 500;
        //     const yScale = d3.scaleLinear()
        //         .domain([0, max])
        //         .range([this.height + this.margin.top, 0]);
        //     const colorScale = d3.scaleOrdinal()
        //         .domain(this.selectedVehicles)
        //         .range(d3.schemeSet3);

        //     const xAxis = d3.axisBottom()
        //                 .scale(xScale);
        //     const yAxis = d3.axisLeft()
        //                 .scale(yScale)
        //                 .ticks(8); 

        //     // const tooltip = d3.select('#tooltip')
        //     //     .style('opacity', 0)
        //     //     .attr('class', 'tooltip')
        //     //     .style('background-color', 'white')
        //     //     .style('border', 'solid')
        //     //     .style('border-width', '1px')
        //     //     .style('border-radius', '5px')
        //     //     .style('padding', '10px');

        //     // const mouseover = function (event, d) {
        //     //     const vehicle = d3.select(this.parentNode).datum().key;
        //     //     const vehicleDuration = d.data[vehicle];
        //     //     tooltip
        //     //         .html('vehicle: ' + vehicle + '<br>Duration: ' + vehicleDuration)
        //     //         .style('opacity', 1);
        //     // };
        //     // const mousemove = function (event, d) {
        //     //     tooltip
        //     //         .style('left', event.layerX + 15 + 'px')
        //     //         .style('top', event.layerY + 'px');
        //     // };
        //     // const mouseleave = function (event, d) {
        //     //     tooltip
        //     //         .style('opacity', 0);
        //     // };

        //     const g = d3.select(`#${this.chartName}`);
        //     g
        //         .selectAll('g')
        //         .data(this.chartData)
        //         .join('rect')
        //         .attr('x', d => xScale(d.id))
        //         .attr('width', xScale.bandwidth() - 5)
        //         .attr('y', d => yScale(d[ref.chartDataType]) + this.margin.top)
        //         .attr('fill', d => colorScale(d.id))
        //         .attr('height', d => this.height - yScale(d[ref.chartDataType]));
        //         // .on('mouseover', mouseover)
        //         // .on('mousemove', mousemove)
        //         // .on('mouseleave', mouseleave);
                        
        //     g.append('g')
        //         .call(xAxis)
        //         .style('transform', `translateY(${this.containerHeight - this.margin.bottom}px)`);
        //     g.append('g')
        //         .call(yAxis)
        //         .attr('transform', `translate(${this.margin.left}, 0)`);

        //     const yLabel = this.chartDataType === 'total_duration' ? 'Usage Duration (minutes)' : 'Idle Duration (minutes)';
        //     g.append('text')
        //         .text(yLabel)
        //         .classed('y-axis-label', true)
        //         .attr('text-anchor', 'end')
        //         .attr('transform', 'rotate(-90) translate(-70, -15)')
        //         .style('font-size', '15px');
        // },
        clearChart() {
            d3.select(`#${this.chartName}`).selectAll('*').remove();
        },
        getDatesInRange(startDate, endDate) {
            const date = new Date(startDate.getTime());
            const dates = [];

            while (date <= endDate) {
                const newDate = new Date(date);
                const newDateStr = (newDate.getMonth() + 1) + '/' + newDate.getDate();
                dates.push(newDateStr);
                date.setDate(date.getDate() + 1);
            }  
            return dates;
        }
    },
    mounted() {
        d3.select('#dept-svg')
            .attr('height', this.containerHeight)
            .attr('width', this.containerWidth + 100);

        this.colorScale = d3.scaleOrdinal()
                .domain(this.selectedVehicles)
                .range(d3.schemeDark2);

        this.renderDeptChart();
    }
};

</script>
<style>
.y-axis-label {
    font-size: 12px;
}
</style>
