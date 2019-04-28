<template>
  <div class="hello">
    <h1>{{ msg }}</h1>

  <contenter v-bind:num="num" v-on:incre="increment" v-on:decre="decrenemnt"></contenter>
    <p>parent:{{num}}</p>
    <!--为num 绑定一个动态的变量-->
  </div>
</template>

<script>
  import contenter from './contenter'
export default {
  name: 'HelloWorld',
  data () {
    return {
      num:10,
      msg: 'Welcome to Your Vue.js App'
    }


    },components:{
    contenter,
    methods:{
      increment(){
        //自组件向父组件传递数据必须用emit
        this.$emit('incre');
      },
      decrenemnt(){
        this.$emit('decre');
      }

    }
  }
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
