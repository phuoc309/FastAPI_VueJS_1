import Vue from 'vue'
import App from './App.vue'
import Toasted from "vue-toasted";
//import "vue-toast-notification/dist/index.css"
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'
//import router from './router';
import Books from './components/Books.vue'
import BorrowBooks from './components/BorrowBooks.vue'
// import BorrowingBooks from './components/BorrowingBooks.vue'
import LoginForm from './views/Login.vue';
//import * as VueRouter from 'vue-router';
Vue.config.productionTip = false

Vue.use(VueRouter)
const router = new VueRouter({
  mode: "history",
  routes: [
    { name: "admin", component: Books, path: "/home"},
    { name: "user", component: BorrowBooks, path: "/"},
    { name: "login", component: LoginForm, path: "/login"}
  ]
});
Vue.use(Toasted, {
  queue: false,
  duration: 2000,
  position: 'bottom-center', // ['top-right', 'top-center', 'top-left', 'bottom-right', 'bottom-center', 'bottom-left']
  theme: 'bubble', // ['toasted-primary', 'outline', 'bubble']
  iconPack: 'material', // ['material', 'fontawesome', 'mdi', 'custom-class', 'callback']
});
new Vue({
  vuetify,
  router,
  render: h => h(App),
}).$mount('#app')
