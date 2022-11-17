<template>
    <div id='tooltip'>
    </div>
    <svg :viewBox="viewBox">
        <g v-bind:id="chartName" transform="translate(35, 5)"> </g>
    </svg>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'PanelChart',
    props: {
        chartData: {
            required: true,
            type: Array,
        },
        chartName: {
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
            innerClass: `${this.chartName}-data`,
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
        renderChart: function () {
            if (this.chartName === 'vehicleDrivingDuration') {
                return this.renderDrivingDurationChart;
            } else if (this.chartName === 'deptDrivingDuration') {
                return this.renderDeptVehicleUsageChart;
            } else {
                return this.renderDrivingDurationChart;
            }
        },
    },
    watch: {
        chartData: function () {
            this.clearChart();
            if (typeof this.renderChart === 'function') {
                this.renderChart();
            }       
        },
    },
    methods: {
        renderDrivingDurationChart() {
            const xScale = d3.scaleBand()
                .domain(this.getDatesInRange(this.fromDate, this.toDate))
                .range([this.width, this.margin.left])
                .padding(0.3);
            const max = this.chartData.length > 0 ? d3.max(this.chartData, d => d.total_duration) : 500;
            const yScale = d3.scaleLinear()
                .domain([0, max])
                .range([this.height + this.margin.top, 0]);

            const xAxis = d3.axisBottom()
                        .scale(xScale);
            const yAxis = d3.axisLeft()
                        .scale(yScale)
                        .ticks(8); 

            const g = d3.selectAll(`#${this.chartName}`);
            g.append('g')
                .classed(this.innerClass, true)
                .call(xAxis)
                .style('transform', `translateY(${this.containerHeight - this.margin.bottom}px)`);
            g.append('g')
                .classed(this.innerClass, true)
                .call(yAxis)
                .attr('transform', `translate(${this.margin.left}, 0)`);
            g
                .selectAll('rect')
                .data(this.chartData)
                .join('rect')
                .attr('x', (d) => {
                    const tripDate = new Date(d.date);
                    const dateStr = tripDate.getMonth() + '/' + tripDate.getDate();
                    return xScale(dateStr);
                })
                .attr('width', xScale.bandwidth() - 5)
                .attr('y', d => yScale(d.total_duration) + this.margin.top)
                .attr('fill', 'lightseagreen')
                .attr('height', d => this.height - yScale(d.total_duration));
            g.append('text')
                .text('Driving Duration (minutes)')
                .classed('y-axis-label', true)
                .attr('text-anchor', 'end')
                .attr('transform', 'rotate(-90) translate(-30, -10)');
        },
        renderDeptVehicleUsageChart() {
            if (this.chartData.length === 0) {
                return;
            }
            // const data = this.chartData.map(el => {
            //     const newEl = {};
            //     const tripDate = new Date(el.date);
            //     const dateStr = tripDate.getMonth() + '/' + tripDate.getDate();
            //     newEl.date = dateStr;
            //     return newEl;
            // });
            const dates = this.getDatesInRange(this.fromDate, this.toDate);
            const uniqueVehicles = [...new Set(this.chartData.map(item => item.vehicle))];
            const dateData = dates.map(el => {
                const dataPoint = { date: el };
                uniqueVehicles.forEach(vehicle => {
                    dataPoint[vehicle] = 0;
                });
                const tripsOnDate = this.chartData.filter(pt => {
                    const tripDate = new Date(pt.date);
                    const dateStr = tripDate.getMonth() + '/' + tripDate.getDate();
                    return dateStr === el;
                });
                let durationSum = 0;
                tripsOnDate.forEach(trip => {
                    dataPoint[trip.vehicle] = trip.driving_duration;
                    durationSum += trip.driving_duration;
                });
                dataPoint.sum = durationSum;
                return dataPoint; 
            });

            // const data = uniqueVehicles.flatMap(vehicle => dateData.map(d => ({ date: d.date, vehicle, duration: d[vehicle] })));
            const stackGen = d3.stack()
                .keys(uniqueVehicles)
                .order(d3.stackOrderNone)
                .offset(d3.stackOffsetNone);

            const stack = stackGen(dateData);
            console.log(uniqueVehicles);
            console.log(dateData);
            console.log(stack);
            const xScale = d3.scaleBand()
                .domain(dates)
                .range([this.width, this.margin.left])
                .padding(0.3);

            const max = dateData.length > 0 ? d3.max(dateData, d => d.sum) : 500;
            const yScale = d3.scaleLinear()
                .domain([0, max])
                .range([this.height + this.margin.top, 0]);
            const colorScale = d3.scaleOrdinal()
                .domain(uniqueVehicles)
                .range(d3.schemeSet3);

            const xAxis = d3.axisBottom()
                        .scale(xScale);
            const yAxis = d3.axisLeft()
                        .scale(yScale)
                        .ticks(8); 

            const tooltip = d3.select('#tooltip')
                .style('opacity', 0)
                .attr('class', 'tooltip')
                .style('background-color', 'white')
                .style('border', 'solid')
                .style('border-width', '1px')
                .style('border-radius', '5px')
                .style('padding', '10px');

            const mouseover = function (event, d) {
                console.log(event);
                
                const vehicle = d3.select(this.parentNode).datum().key;
                const vehicleDuration = d.data[vehicle];
                console.log(vehicle);
                tooltip
                    .html('vehicle: ' + vehicle + '<br>Duration: ' + vehicleDuration)
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

            const g = d3.select(`#${this.chartName}`);
            g
                .selectAll('g')
                .data(stack)
                .join('g')
                .attr('fill', d => colorScale(d.key))
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
                .classed(this.innerClass, true)
                .call(xAxis)
                .style('transform', `translateY(${this.containerHeight - this.margin.bottom}px)`);
            g.append('g')
                .classed(this.innerClass, true)
                .call(yAxis)
                .attr('transform', `translate(${this.margin.left}, 0)`);

            g.append('text')
                .text('Driving Duration (minutes)')
                .classed('y-axis-label', true)
                .attr('text-anchor', 'end')
                .attr('transform', 'rotate(-90) translate(-30, -10)');
        },
        clearChart() {
            d3.selectAll(`.${this.innerClass}`).remove();
        },
        getDatesInRange(startDate, endDate) {
            const date = new Date(startDate.getTime());

            const dates = [];

            while (date <= endDate) {
                const newDate = new Date(date);
                const newDateStr = newDate.getMonth() + '/' + newDate.getDate();
                dates.push(newDateStr);
                date.setDate(date.getDate() + 1);
            }  
            return dates;
        }
    },
    mounted() {
        if (this.chartName === 'vehicleDrivingDuration') {
            return this.renderDrivingDurationChart();
        } else if (this.chartName === 'deptDrivingDuration') {
            return this.renderDeptVehicleUsageChart();
        } else {
            return this.renderDrivingDurationChart();
        }
    }
};

</script>
<style>
.y-axis-label {
    font-size: 12px;
}
</style>
