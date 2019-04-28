<template>
  <div id="app">
    <!--<img src="./assets/logo.png">-->
    <!--将视图切换为三份-->
    <router-view class="main"></router-view>
    <router-view class="left" name="title"></router-view>
    <router-view class='right' name="img"></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  .left,.right{
    width: 48%;
    height: auto;
    float: left;
    border: 1px solid gray;
  }
}
</style>
