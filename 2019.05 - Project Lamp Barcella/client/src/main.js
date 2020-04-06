// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import App from './App';
import VueSocketio from 'vue-socket.io';
import io from 'socket.io-client'
import router from './router';
import moment from 'moment';

const SERVER_HOST = '127.0.0.1';

export const socket = io("http://" + SERVER_HOST + ":5000")   //here!
socket.on('connection', () => {
    console.log("connected");
})
Vue.use(VueSocketio, socket)
console.log("imports done...");


Vue.use(BootstrapVue);

Vue.config.productionTip = false;

Vue.prototype.$apiBaseUrl = 'http://' + SERVER_HOST + ':5000';            //here!
Vue.prototype.$websocketUrl = 'ws://' + SERVER_HOST + ':5000/esperia';    //here!
Vue.prototype.$arduinoStatus = [];
Vue.prototype.$lampCurrentColors = [];

Vue.filter('formatDate', function(value) {
    if (value==0) {
        return '∞'
    }
    if (value) {
        var now = new Date(value * 1000);
        return now.toLocaleTimeString();
    }
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',

});
