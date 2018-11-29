import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueResource from 'vue-resource'

/* eslint-disable no-new */

Vue.use(VueResource)
Vue.use(ElementUI)

new Vue({
  el: '#app',
  template: '<App/>',
  components: { App }
})
