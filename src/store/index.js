import { createStore } from 'vuex';
import { ref } from 'vue';

export default createStore({
    state: {
        selectedVehicle: 'UFOU6379',
        selectedTrips: [],
        selectedDept: '',
        minDate: ref(new Date('2022-09-27T00:00:00')),
        maxDate: ref(new Date('2022-09-29T00:00:00')),
        fromDate: ref(new Date('2022-09-27T00:00:00')),
        toDate: ref(new Date('2022-09-29T00:00:00')),
        showVehicles: true,
        showVehicleList: true,

        plan: 'p20',
        selectedBus: '1025',
        selectedRoute: '2X',
        selectedChargingStation: '7',
        time: '01:40',
        showBusses: true,
        routeFocused: false,
        routeFocusedNum: -1,
        bussesToShow: null,
        busLocations: {
            type: 'FeatureCollection',
            features: [{
                type: 'Feature',
                properties: { 
                    id: -1,
                    converted: 0,
                    atStation: true,
                    remainingCharge: 100,
                    show: true
                },
                geometry: {
                    type: 'Point',
                    coordinates: [0, 0]
                }
            }]
        },
    },
    getters: {},
    mutations: {
        CHANGE_SELECTED_VEHICLE(state, vehicleId) {
            state.selectedVehicle = vehicleId;
        },
        CHANGE_SELECTED_DEPT(state, dept) {
            state.selectedDept = dept;
        },
        CHANGE_FROM_DATE(state, date) {
            state.fromDate = date;
        },
        CHANGE_TO_DATE(state, date) {
            state.toDate = date;
        },
        CHANGE_SELECTED_TRIPS(state, trips) {
            state.selectedTrips = trips;
        },
        CHANGE_PANEL_VIEW(state, showVehicles) {
            state.showVehicles = showVehicles;
        },
        CHANGE_LIST_VIEW(state, showVehicleList) {
            state.showVehicleList = showVehicleList;
        },

        CHANGE_PLAN(state, plan) {
            state.plan = plan;
        },
        CHANGE_SELECTED_BUS(state, busId) {
            state.selectedBus = busId;
        },
        CHANGE_SELECTED_ROUTE(state, routeId) {
            state.selectedRoute = routeId;
        },
        CHANGE_SELECTED_CHARGING_STATION(state, stationId) {
            state.selectedChargingStation = stationId;
        },
        CHANGE_TIME(state, time) {
            state.time = time;
        },
        CHANGE_SHOW_BUSSES(state, showBusses) {
            state.showBusses = showBusses;
        },
        CHANGE_BUS_LOCATIONS(state, busLocations) {
            state.busLocations = busLocations;
        },
        CHANGE_BUSESS_TO_SHOW(state, bussesToShow) {
            state.bussesToShow = bussesToShow;
        },
        CHANGE_ROUTE_FOCUSED(state, routeFocused) {
            state.routeFocused = routeFocused;
        },
        CHANGE_ROUTE_FOCUSED_NUM(state, routeFocusedNum) {
            state.routeFocusedNum = routeFocusedNum;
        }
    },
    actions: {
        changeVehicle({ commit }, payload) {
            commit('CHANGE_SELECTED_VEHICLE', payload);
        },
        changeDept({ commit }, payload) {
            commit('CHANGE_SELECTED_DEPT', payload);
        },
        changeFromDate({ commit }, payload) {
            commit('CHANGE_FROM_DATE', payload);
        },
        changeToDate({ commit }, payload) {
            commit('CHANGE_TO_DATE', payload);
        },
        changeSelectedTrips({ commit }, payload) {
            commit('CHANGE_SELECTED_TRIPS', payload);
        },
        changePanelView({ commit }, payload) {
            commit('CHANGE_PANEL_VIEW', payload);
        }, 
        changeListView({ commit }, payload) {
            commit('CHANGE_LIST_VIEW', payload);
        }, 

        changePlan({ commit }, payload) {
            commit('CHANGE_PLAN', payload);
        },
        changeRoute({ commit }, payload) {
            commit('CHANGE_SELECTED_ROUTE', payload);
        },
        changeBus({ commit }, payload) {
            commit('CHANGE_SELECTED_BUS', payload);
        },
        changeStation({ commit }, payload) {
            commit('CHANGE_SELECTED_CHARGING_STATION', payload);
        },
        changeTime({ commit }, payload) {
            commit('CHANGE_TIME', payload);
        },
        changeShowBusses({ commit }, payload) {
            commit('CHANGE_SHOW_BUSSES', payload);
        },
        changeBusLocations({ commit }, payload) {
            commit('CHANGE_BUS_LOCATIONS', payload);
        },
        changeBussesToShow({ commit }, payload) {
            commit('CHANGE_BUSESS_TO_SHOW', payload);
        },
        changeRouteFocused({ commit }, payload) {
            commit('CHANGE_ROUTE_FOCUSED', payload);
        },
        changeRouteFocusedNum({ commit }, payload) {
            commit('CHANGE_ROUTE_FOCUSED_NUM', payload);
        }
    }
  });
