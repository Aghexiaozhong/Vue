<template>
    <!--<div>这是商品列表页面-->
      <!--<span>{{$route.params.goodsId}}</span>-->
      <!--<span>{{$route.params.username}}</span>-->
      <!--<router-link to="/goods/title">显示商品标题</router-link>-->
      <!--<router-link to="/goods/img">显示商品图片</router-link>-->
     <!--<div>-->
      <!--<router-view></router-view>-->
       <!--&lt;!&ndash;用来渲染子组件&ndash;&gt;-->
       <!--<router-link v-bind:to="{name:'cart',params:{cartId:123}}">跳转到购物车页面</router-link>-->
       <!--&lt;!&ndash;<button @click="jump">&#45;&#45; 跳转到购物车页面-&#45;&#45;</button>&ndash;&gt;-->
     <!--</div>-->
    <!--</div>-->


  <!--需要一个根元素-->
  <div>
    <!--标签名不能大写-->
    <nav-header></nav-header>
   <nav-bread>
     <!--slot的属性值得与navbread组件的slot标签的name值相同-->
     <span slot="bread">Goods</span>
   </nav-bread>
    <div class="accessory-result-page accessory-page">
      <div class="container">
        <div class="filter-nav">
          <span class="sortby">Sort by:</span>
          <a href="javascript:void(0)" class="default cur">Default</a>
          <a href="javascript:void(0)" class="price" @click="sortGoods">Price
            <svg class="icon icon-arrow-short" v-bind:class="{'sort-up':!sortFlag}"><use xlink:href="#icon-arrow-short"></use></svg></a>
         <!--使得下面的Filter by 实现当页面缩小时，价格过滤依然存在-->
          <a href="javascript:void(0)" class="filterby stopPop" @click="showFilter">Filter by</a>
        </div>
        <div class="accessory-result">
          <!-- filter 当窗口缩小至Pc端的最小范围是，价格过滤这一块会自动隐藏，设置一下，使其依然显示-->
          <div class="filter stopPop" id="filter" v-bind:class="{'filterby-show':filterBy}">
            <dl class="filter-price">
              <dt>Price:</dt>
              <dd><a href="javascript:void(0)" v-bind:class="{'cur':priceChecked == 'all'}" @click="priceChecked == 'all'">All</a></dd>
              <dd v-for="(item,index) in priceFilter">
                <a href="javascript:void(0)" v-bind:class="{'cur':priceChecked== index}" @click="setPriceFilter(index)">{{item.startPrice}} - {{item.endPrice}}</a>
              </dd>

            </dl>
          </div>

          <!-- search result accessories list -->
          <div class="accessory-list-wrap">
            <div class="accessory-list col-4">
              <ul>
                <li v-for="(item,index) in goodsList">
                  <div class="pic">
                    <!--需要动态绑定src元素，等加载完才确定链接 这样的话里面相当于js,如果写字符串需要加引号-->
                    <a href="#"><img v-lazy="'/static/'+item.productImage" alt=""></a>
                  </div>
                  <div class="main">
                    <div class="name">{{item.productName}}</div>
                    <div class="price">{{item.salePrice}}</div>
                    <div class="btn-area">
                      <a href="javascript:;" class="btn btn--m" @click="addCart(item.productId)">加入购物车</a>
                    </div>
                  </div>
                </li>

              </ul>
              <div v-infinite-scroll="loadMore" class="load-more" infinite-scroll-disabled="busy" infinite-scroll-distance="30">
                <img src="./../assets/loading-spinning-bubbles.svg" v-show="loading">
                <!--通过控制开关，来决定图片（loading文件夹里的各种loading图片）的显示和隐藏-->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--v-show 的功能： 当overLayFlag的值为falase的时候，就不显示内容，为true的时候显示-->
    <div class="md-overlay" v-show="overLayFlag" @click="closepop"></div>
    <!---->
    <modal v-bind:mdShow="mdShow" v-on:close="closeModal">
      <p slot="message">
        请先登录，否则无法加入到购物车中
      </p>
      <div slot="btnGroup">
        <a class="btn btn--m" href="javascript:;" @click="mdShow=false">关闭</a>
      </div>
    </modal>
    <modal v-bind:mdShow="mdShowCart" v-on:close="closeModal">
      <p slot="message">
        <svg class="icon-status-ok">

          <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#icon-status-ok"></use>

        </svg>
        <span>加入购物车成功!</span>
      </p>
      <div slot="btnGroup">
        <a class="btn btn--m" href="javascript:;" @click="mdShowCart=false">继续购物</a>
        <router-link class="btn btn--m" href="javascript:;" to="/cart">查看购物车</router-link>
      </div>
    </modal>
    <nav-footer></nav-footer>
  </div>
</template>
<style>
  .load-more{
    text-align: center;
    height: 100px;
    line-height: 100px;

  }
  .sort-up{
    transform:rotate(180deg);
    transition: all .3s ease-out;
  }
  .icon-arrow-short{
    width: 11px;
    height: 11px;
    transition: all .3s ease-out;
  }
  .btn:hover{
    background-color: #ffe5e6;
    transition: all .3s ease-out;
  }
</style>
<script>
  import './../assets/css/base.css'
  import './../assets/css/product.css'

  //导入其他组件  起的名字不能喝H5标签重复了
  import NavHeader from '@/components/NavHeader.vue'
  import NavFooter from '@/components/NavFooter.vue'
  import NavBread from '@/components/NavBread.vue'
  import axios from 'axios'
  import Modal from './../components/Model'



    export default {
        name: "goos-list",
        //防止组件之间的数据相互影响
        data(){
          return {

            goodsList:[],
            priceFilter:[
              {
                startPrice:'0.00',
                endPrice:'100.00'
              },
              {
                startPrice:'100.00',
                endPrice:'500.00'
              },{
                startPrice:'500.00',
                endPrice:'1000.00'
              },{
                startPrice:'1000.00',
                endPrice:'2000.00'
              }
            ],
            //控制选择的是哪一项
            priceChecked:'all',
            filterBy:false,
            overLayFlag:false,
            //定义一个默认的排序
            sortFlag:true,
            page:1,
            pageSize:8,
            busy:true // 默认是禁用的
            ,loading:false , // 设置加载中那个样式图片（loading文件夹里的各种loading图片），默认是不显示的
            mdShow:false,  //默认不显示这个弹框，当报错的时候在显示
            mdShowCart:false   //默认不显示点击添加购物车按钮之后的弹框提示

          }
        },
      components:{
          NavHeader,
          NavFooter,
          NavBread,
          Modal
      },
      //定义一个初始化的方法
      mounted:function () {
        this.getGoodsList();

      },
      methods: {

        getGoodsList(flag){
          var param = {
            page:this.page,
            pageSize:this.pageSize,
            sort:this.sortFlag?1:-1,
            priceLevel:this.priceChecked
          };
          //接口请求完毕之前，把图片（loading文件夹里的各种loading图片）显示出来，因为还在加载中
          this.loading = true;
          axios.get('/goods/list',{params:param}).then(result=>{

            var res  = result.data;
            //响应之后，把图片（loading文件夹里的各种loading图片）关闭显示
            this.loading = false;
            if(res.status == '0'){
              if(flag){
                //如果是分页的话，则吧数据累加
                this.goodsList = this.goodsList.concat(res.result.list);
                if(res.result.count == 0){
                  this.busy = true;  // 当已经请求完所有的数据之后，吧busy改为true,使得后续的鼠标滚动加载事件失效
                }else{
                  this.busy = false; // 如果还有数据，则继续滚动

                }
              }else{
                this.goodsList = res.result.list;
                this.busy = false;
              }

            }else{
              this.goodsList = [];
            }

          });

        },
        //点击filter by 显示价格过滤
        showFilter(){
          this.filterBy = true;
          this.overLayFlag = true;
        },
        //点击遮罩，则使得filter隐藏

        setPriceFilter(index){
          //实现价格过滤
          this.priceChecked = index;
          this.page = 1;
          this.getGoodsList();

          this.closepop();
        },
        closepop(){
          this.filterBy = false;
          this.overLayFlag = false;
        },
        //定义排序方法  当点击price  排序方式就会和原来的相反
        sortGoods(){
          this.sortFlag = !this.sortFlag;
          this.page =1;
          this.getGoodsList();
        },
        //当鼠标滚动的时候需要加载的方法
        loadMore(){

          //当滚动鼠标的时候，保证第一个资源请求加载完在执行第二个请求，这样会减小服务器压力
          this.busy = true;  //在页面请求成功之前，禁用鼠标滚动再去加载其他的事件
          setTimeout(()=>{
            this.page ++;
            this.getGoodsList(true);


          },5000);
        },
        addCart(productId){
          axios.post('/goods/addCart',{
            productId:productId
          }).then((response)=>{
              let res = response.data;
            if(res.status == '0'){
              this.mdShowCart = true;

              this.$store.commit("updateCartCount",1);   //点击一次添加购物车，商品总数加1
            }else{
              this.mdShow = true;
            }
          }
          );
        },
        closeModal(){
            this.mdShow = false;

        }
      }
      }

</script>

<style scoped>

</style>
