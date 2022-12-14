<template>
    <div id='tooltip'>
    </div>
    <svg id="vehicle-svg">
        <g v-bind:id="chartName" transform="translate(27, 5)"> </g>
    </svg>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'VehiclePanelChart',
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
            chartName: 'vehicle-chart',
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
        selectedVehicles: function () {
          return this.$store.state.selectedDeptVehicles;
        },
        yLabel: function () {
            if (this.chartDataType === 'total_duration') {
                return 'Total Usage Duration (minutes)';
            } else if (this.chartDataType === 'idle_duration') {
                return 'Idle Duration (minutes)';
            } else if (this.chartDataType === 'distance') {
                return 'Distance Traveled (miles)';
            } else if (this.chartDataType === 'driving_duration') {
                return 'Driving Duration (minutes)';
            } else {
                return 'Total Usage Duration (minutes)';
            }
        }
    },
    watch: {
        // When the chart data changes, update the chart
        chartData: function () {
            this.clearChart();
            return this.renderVehicleChart();    
        },
        chartDataType: function () {
            this.clearChart();
            return this.renderVehicleChart();
        },
    },
    methods: {
        // renderVehicleChart() {
        //     const ref = this;
        //     console.log(this.getDatesInRange(this.fromDate, this.toDate));
        //     const xScale = d3.scaleBand()
        //         .domain(this.getDatesInRange(this.fromDate, this.toDate))
        //         .range([this.margin.left, this.width])
        //         .padding(0.3);
        //     const max = this.chartData.length > 0 ? d3.max(this.chartData, d => d[ref.chartDataType]) : 500;
        //     const yScale = d3.scaleLinear()
        //         .domain([0, max])
        //         .range([this.height + this.margin.top, 0]);

        //     const xAxis = d3.axisBottom()
        //                 .scale(xScale);
        //     const yAxis = d3.axisLeft()
        //                 .scale(yScale)
        //                 .ticks(8); 

        //     const g = d3.selectAll(`#${this.chartName}`);
        //     g.append('g')
        //         .call(xAxis)
        //         .style('transform', `translateY(${this.containerHeight - this.margin.bottom}px)`);
        //     g.append('g')
        //         .call(yAxis)
        //         .attr('transform', `translate(${this.margin.left}, 0)`);
        //     g
        //         .selectAll('rect')
        //         .data(this.chartData)
        //         .join('rect')
        //         .attr('x', (d) => {
        //             const tripDate = new Date(d.date);
        //             const dateStr = tripDate.getMonth() + '/' + tripDate.getDate();
        //             return xScale(dateStr);
        //         })
        //         .attr('width', xScale.bandwidth() - 5)
        //         .attr('y', d => yScale(d[ref.chartDataType]) + this.margin.top)
        //         .attr('fill', 'lightseagreen')
        //         .attr('height', d => this.height - yScale(d[ref.chartDataType]));

        //     const yLabel = this.chartDataType === 'total_duration' ? 'Usage Duration (minutes)' : 'Idle Duration (minutes)';
        //     g.append('text')
        //         .text(yLabel)
        //         .classed('y-axis-label', true)
        //         .attr('text-anchor', 'end')
        //         .attr('transform', 'rotate(-90) translate(-70, -15)')
        //         .style('font-size', '15px');
        // },
        renderVehicleChart() {
            const ref = this;
            const rangeDates = this.getDatesInRange(this.fromDate, this.toDate);
            const data = this.chartData.map(el => {
                const newEl = {};
                const tripDate = new Date(el.date);
                newEl.date = (tripDate.getMonth() + 1) + '/' + tripDate.getDate();
                newEl.total_duration = el.total_duration;
                newEl.idle_duration = el.idle_duration;
                newEl.distance = el.distance;
                newEl.driving_duration = el.driving_duration;

                return newEl;
            });
            data.sort((a, b) => (Date(a.date) > Date(b.date)) ? -1 : 1);
            if (data.length < rangeDates.length) {
                    const currDates = data.map(el => el.date);
                    rangeDates.forEach((date, i) => {
                        if (!currDates.includes(date)) {
                            data.splice(i, 0, {
                                date: date,
                                idle_duration: 0,
                                total_duration: 0,
                                driving_duration: 0,
                                distance: 0
                            });
                        }
                    });
            }
            console.log(data);
            const xScale = d3.scalePoint()
                .domain(rangeDates)
                .range([this.margin.left, this.width]);
                
            const max = this.chartData.length > 0 ? d3.max(this.chartData, d => d[ref.chartDataType]) : 500;
            const yScale = d3.scaleLinear()
                .domain([0, max])
                .range([this.height + this.margin.top, 0])
                .nice();

            const ticks = Math.floor(rangeDates.length / 10);
            const xAxis = d3.axisBottom(xScale)
                        .tickValues(xScale.domain().filter((d, i) => { return !(i % ticks); }));
            const yAxis = d3.axisLeft()
                        .scale(yScale)
                        .ticks(8); 

            const g = d3.selectAll(`#${this.chartName}`);
            g.append('g')
                .call(xAxis)
                .style('transform', `translateY(${this.containerHeight - this.margin.bottom}px)`);
            g.append('g')
                .call(yAxis)
                .attr('transform', `translate(${this.margin.left}, 0)`);

            const lineGenerator = d3
                .line()
                .x((d) => xScale(d.date))
                .y((d) => yScale(d[ref.chartDataType]));
            const lineChart = g.append('g').append('path').attr('class', 'line-chart');
            lineChart
                .datum(data)
                .attr('d', lineGenerator);

            g.append('text')
                .text(this.yLabel)
                .classed('y-axis-label', true)
                .attr('text-anchor', 'end')
                .attr('transform', 'rotate(-90) translate(-70, -15)')
                .style('font-size', '15px');
        },
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
        d3.select('#vehicle-svg')
            .attr('height', this.containerHeight)
            .attr('width', this.containerWidth + 100);

        this.renderVehicleChart();
    }
};

</script>
<style>
.y-axis-label {
    font-size: 12px;
}
.line-chart {
      stroke: lightseagreen;
      stroke-width: 2;
      fill: none;
    }
</style>
