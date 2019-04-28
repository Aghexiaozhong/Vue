import Vue from 'vue'
import Router from 'vue-router'
//import HelloWorld from '@/components/HelloWorld'
import goodsList from '@/views/goodsList.vue'
//@  相当于　src/
// import Title from '@/views/Title'
// import Imgs from '@/views/imgs'
// import cart from '@/views/cart'
import Cart from '@/views/cart.vue'
import Address from '@/views/Address.vue'
import OrderConfirm from '@/views/OrderConfirm.vue'
import OrderSuccess from '@/views/OrderSuccess.vue'
Vue.use(Router);

export default new Router({
  routes: [
    {
      //path: '/goods/:goodsId/user/:username',  //动态路由   v-router 就是对history的封装
      path: '/',
      name: 'goodslist',
      component: goodsList
    },
    {

      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    {

      path: '/address',
      name: 'Address',
      component: Address
    },
    {

      path: '/orderConfirm',
      name: 'OrderConfirm',
      component: OrderConfirm
    },
    {

      path: '/OrderSuccess',
      name: 'OrderSuccess',
      component: OrderSuccess
    }




      //不同的名字对应不同的组件
      // children:[
      //   {
      //   path:'/cart/:cartId',
      //     name:'cart',
      //     component:cart
      //   }
      // ]




  ]
})
