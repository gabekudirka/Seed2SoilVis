// Contains all state variables
import { createStore } from 'vuex';
import { ref } from 'vue';

export default createStore({
    state: {
        selectedVehicle: 'UFOU6379',
        selectedTrips: [],
        selectedDept: '',
        selectedDeptVehicles: [],
        minDate: ref(new Date('2022-09-01T00:00:00')),
        maxDate: ref(new Date('2022-10-31T00:00:00')),
        fromDate: ref(new Date('2022-09-15T00:00:00')),
        toDate: ref(new Date('2022-09-25T00:00:00')),
        showVehicles: true,
        showVehicleList: true,
        showMapView: true,
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
        CHANGE_MAIN_VIEW(state, showMapView) {
            state.showMapView = showMapView;
        },
        CHANGE_SELECTED_DEPT_VEHICLES(state, selectedDeptVehicles) {
            state.selectedDeptVehicles = selectedDeptVehicles;
        },
    },
    actions: {
        changeVehicle({ commit }, payload) {
            commit('CHANGE_SELECTED_VEHICLE', payload);
        },
        changeDept({ commit }, payload) {
            commit('CHANGE_SELECTED_DEPT', payload);
        },
        changeDeptVehicles({ commit }, payload) {
            commit('CHANGE_SELECTED_DEPT_VEHICLES', payload);
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
        changeMainView({ commit }, payload) {
            commit('CHANGE_MAIN_VIEW', payload);
        },
    }
  });
