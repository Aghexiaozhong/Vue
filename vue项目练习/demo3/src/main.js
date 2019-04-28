// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
//在此接收utils.js里面的函数
//import {sum,minve} from "./utils";

//console.log(`sum:${sum(3,5)}`);
Vue.config.productionTip = false;
//导入图片懒加载的插件  图片懒加载避免耗用大量的静态资源
import VueLazyLoad from 'vue-lazyload'
//这个是关于滚动条的
import infiniteCroll from 'vue-infinite-scroll'
//定义自己的vuex文件系统
Vue.use(Vuex);
const store = new Vuex.Store({
    state:{
      //用户名和购物车数量在所有组件都可以使用
      nickName:'',
      cartCount:0
    },
  //用来改变状态
    mutations:{
      updateUserInfo(state,nickName){
        state.nickName = nickName;
      },
      updateCartCount(state,cartCount){
        state.cartCount += cartCount;
      },
      initCartCount(state,cartCount){
        state.cartCount = cartCount;
      }
    }
});
import Vuex from 'vuex'
//导入全局过滤器  这里是价格过滤器
import {currency} from './util/current'

Vue.filter("currency",currency);


Vue.use(
  infiniteCroll
);
Vue.use(VueLazyLoad,{
  //指定在图片加载之前有个loading 的效果
  loading:"/static/loading-svg/loading-bars.svg"
});
/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
});
