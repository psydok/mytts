import {createApp} from 'vue';
import App from './App.vue';
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import router from "./router/router";

const myApp = createApp(App);
myApp.use(router);
myApp.mount('#app');
myApp.config.globalProperties.$filters = {
    round(value) {
        return Number(value).toFixed(2);
    }
}