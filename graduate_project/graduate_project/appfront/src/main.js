import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueResource from 'vue-resource'
import Scrollspy from 'vue2-scrollspy'
import iView from 'iview';
import 'iview/dist/styles/iview.css';

Vue.config.productionTip = false
Vue.prototype.$goRoute = function (index) {
  this.$router.push(index)
}
Vue.use(Scrollspy);
Vue.use(ElementUI);
Vue.use(VueResource);
Vue.use(iView);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
