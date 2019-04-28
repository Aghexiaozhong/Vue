var express = require('express');
var router = express.Router();
//加载util下的utils.js 用来格式化时间的
require('./../util/util');


/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

//对应的二级路由   /users/test  而/   /users　是一级路由
router.get('/test', function(req, res, next) {
  res.send('respond with a test');
});

var User = require('./../models/user');
//登录接口
router.post('/login',(req,res,next)=>{
  var param = {
    userName:req.body.userName,
    userPwd:req.body.userPwd
  };


  User.findOne(param,(err,doc)=>{
    if(err){
      res.json({
        status:'1',
        msg:err.message
      });
    }else{
      if(doc){
        console.log('ok-----------------------------');
        //如果存在用户，则把其写进cookie
        //第一个参数cookie   名字  第二个参数 cookie的值
        res.cookie('userId',doc.userId,{
          path:'/',
          maxAge:1000*60*60
        });
        res.cookie('userName',doc.userName,{
          path:'/',
          maxAge:1000*60*60
        });
        //req.session.user = doc;

        console.log('成功--------------');
        res.json({
          status:'0',
          msg:'',
          result:{
            userName:doc.userName,

          }
        });
      }
    }
  });
});


//登出接口
router.post('/logout',(req,res,next)=>{
  res.cookie('userId','',{
    path:'/',
    maxAge:-1   //使得cookie失效
  });
  res.json({
    status:'0',
    mag:'',
    result:''
  });
});
//校验是否登录
router.get('/checkLogin',(req,res,next)=>{
  if(req.cookies.userId){
    res.json({
      status:'0',
      msg:'',
      result:req.cookies.userName
    });
  }else{
    res.json({
      status:'1',
      msg:'未登录',
      result:''
    });
  }
});

//查询用户的名下购物车列表
router.get('/cartList',(req,res,next)=>{
  var userId = req.cookies.userId;
  User.findOne({userId:userId},(err,doc)=>{
    if(err){
      res.json({
        status:'1',
        msg:err.message,
        result:''
      });
    }else{
      if(doc){
        //取得用户信息
        res.json({
          status:'0',
          msg:'',
          result:doc.cartList
        });
      }
    }
  });
});

//定义购物车删除
router.post('/cartDel',(req,res,next)=>{
  var userId = req.cookies.userId;
  var productId = req.body.productId;
  //删除cartList下的对应的商品id 的子文档
  User.update({userId:userId},{$pull:{'cartList':{'productId':productId}}},(err,doc)=>{
    if(err){
      res.json({
        status:'1',
        msg:err.message,
        result:''
      });
    }else{
      res.json({
        status:'0',
        msg:'删除成功',
        result:'success'
      });
    }
  });

});
//编辑购物车数量

router.post('/cartEdit',(req,res,next)=>{
  var userId = req.cookies.userId,productId = req.body.productId;
  var productNum = req.body.productNum;
  var checked = req.body.checked;
  //第一个参数是更新的条件，第二个是更新操作
  User.update({'userId':userId,'cartList.productId':productId},{
    'cartList.$.productNum':productNum,
    'cartList.$.checked':checked

  },(err,doc)=>{
    if(err){
      res.json({
        status:'1',
        msg:err.message,
        result:''
      });
    }else{
      res.json({
        status:'0',
        msg:'',
        result:'success'
      });
    }
  });



});
//是否选中所有的购物车列表中的商品
router.post('/editCheckAll',(req,res,next)=>{
  var userId = req.cookies.userId;
  var checkAll  = req.body.checkAll?'1':'0';
  User.findOne({userId:userId},(err,user)=>{
    if(err){
      res.json({
        status:'1',
        msg:err.message,
        result:''
      });
    }else{
      if(user) {
        user.cartList.forEach((item) => {
          item.checked = checkAll;
        });

        user.save((err1,doc)=>{
          if(err1){
            res.json({
              status:'1',
              msg:err.message,
              result:''
            });
          }else{
            res.json({
              status:'0',
              msg:'',
              result:'success'
            });
          }
        });
      }

    }
  });
});
//查询用户地址的接口
router.get('/addressList',(req,res,next)=>{
  var userId = req.cookies.userId;
  User.findOne({userId:userId},(err,doc)=>{
    if(err){
      res.json({
        status:'1',
        msg:err.message,
        result:''
      });
    }else{
      res.json({
        status:'0',
        msg:'',
        result:doc.addressList
      });
    }
  });
});

//修改默认地址的接口
router.post('/setDefaultAddress',(req,res,next)=>{
    var userId = req.cookies.userId;
    var addressId = req.body.addressId;
    if(!addressId){
      res.json({
        status:'1003',
        msg:'addressId id null',
        result:''
      });
    }else{
      User.findOne({userId:userId},(err,doc)=>{
        if(err){
          res.json({
            status:'1',
            msg:err.message,
            result:''
          });
        }else{
          var addressList = doc.addressList;
          addressList.forEach(item=>{
                if(item.addressId == addressId){
                    item.isDefault = true;
                }else{
                  item.isDefault = false;
                }
          });
          doc.save((err,doc)=>{
            if(err){
              res.json({
                status:'1',
                msg:err.message,
                result:''
              });
            }
            else{
              res.json({
                status:'0',
                msg:'',
                result:'success'
              });
            }
          });
        }
      });
    }

});

//删除地址的接口
router.post('/delAddress',(req,res,next)=>{
    var userId = req.cookies.userId;
    var addressId = req.body.addressId;
  User.update({userId:userId},{$pull:{'addressList':{'addressId':addressId}}},(err,doc)=>{
    if(err){
      res.json({
        status:'1',
        msg:err.message,
        result:''
      });
    }else{
      res.json({
        status:'0',
        msg:'',
        result:'success'
      });
    }
  });
});
//生产订单接口
router.post('/payMent',(req,res,next)=>{
    var userId = req.cookies.userId,addressId = req.body.addressId;
    var orderTotal =  req.body.orderTotal;
    User.findOne({userId:userId},(err,doc)=>{
      if(err){
        res.json({
          status:'1',
          msg:err.message,
          result:''
        });
      }else{
        var address = '',goodsList = [];
        //获取当前用户的地址信息
        doc.addressList.forEach(item=>{
            if(item.addressId == addressId){
                address = item;
            }
        });
        //获取用户购物车的购买商品
        doc.cartList.filter(item=>{
            if(item.checked == '1'){
              goodsList.push(item);
            }
        });
        //生成订单号
        //设置平台
        var platform = '622';

        var r1 = Math.floor(Math.random()*10);
        var r2 = Math.floor(Math.random()*10);

        var sysDate = new Date().Format('yyyyMMddhhmmss');
        var orderDate = new Date().Format('yyyy-MM-dd hh:mm:ss');
        var orderId = platform + r1 + sysDate + r2;


        //创建订单
        var order = {
          orderId:orderId,
          orderTotal:orderTotal,
          addressInfo:address,
          goodsList:goodsList,
          orderStatus:'1',
          createDate:orderDate
        };
        doc.orderList.push(order);
        doc.save((err1,doc1)=>{
          if(err1){
            res.json({
              status:'1',
              msg:err.message,
              result:''
            });
          }else{
            res.json({
              status:'0',
              msg:'',
              result:{
                orderId:order.orderId,
                orderTotal:order.orderTotal
              }
            });
          }
        });

      }
    });
});

//根据订单id查询订单信息
router.get('/orderDetail',(req,res,next)=>{
    var userId = req.cookies.userId,orderId = req.param('orderId');
    User.findOne({userId:userId},(err,userinfo)=>{
      if(err){
        res.json({
          status:'1',
          msg:err.message,
          result:''
        });
      }else{
        var orderList = userinfo.orderList;
        if(orderList.length>0){
          var orderTotal = 0;
            orderList.forEach(item=>{
                if(item.orderId == orderId){
                    orderTotal += item.orderTotal;

                }
            });
            if(orderTotal > 0 ){
              res.json({
                status:'0',
                msg:'',
                result:{
                  orderId:orderId,
                  orderTotal:orderTotal
                }
              });
            }else{
              res.json({
                status:'120002',
                msg:'无此订单',
                result:''
              });
            }

        }else{
          res.json({
            status:'120001',
            msg:'当前用户未创建订单',
            result:''
          });
        }
      }
    });
});

//获取购物车商品数量
router.get('/getCartCount',(req,res,next)=>{
  if(req.cookies && req.cookies.userId){
    var userId = req.cookies.userId;
    User.findOne({userId:userId},(err,doc)=>{
      if(err){
        res.json({
          status:'1',
          msg:err.message,
          result:''
        });
      }else{
          var cartList = doc.cartList;
          let cartCount = 0;
          cartList.forEach(item=>{
            cartCount += parseInt(item.productNum);
          });
        res.json({
          status:'0',
          msg:'',
          result:cartCount
        });
      }
    });
  }
});
module.exports = router;
