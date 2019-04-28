//拿到以及路由
var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
//加载模型baio
var Goods = require('./../models/goods');
//连接数据库
mongoose.connect('mongodb://127.0.0.1:27017/zhongmall');
mongoose.connection.on('connected',function () {
  console.log('Mongodb connected successs');
});

mongoose.connection.on('error',function () {
  console.log('Mongodb connected fail');
});

mongoose.connection.on('disconnected',function () {
  console.log('Mongodb connected 断开');
});
//分页，价格过滤  商品列表
router.get('/list',function (req,res,next) {
  //排序
  let page = parseInt(req.param('page'));
  let pageSize = parseInt(req.param('pageSize'));
  let priceLevel = req.param('priceLevel');
  let sort = req.param("sort");
  let params = {};
  var priceGt = '',priceLt = '';   // 设置价格区间
  if(priceLevel != 'all'){
    switch (priceLevel){
      case '0':priceGt = 0;priceLt=100;break;
      case '1':priceGt = 100;priceLt=500;break;
      case '2':priceGt = 500;priceLt=1000;break;
      case '3':priceGt = 1000;priceLt=5000;break;
    }
    params = {
      salePrice:{
        $gt:priceGt,
        $lte:priceLt
      }
    }
  }else{
    params = {
      salePrice:{
        $gt:0,
        $lte:2000
      }
    }
  }


  let skip = (page-1)* pageSize;
  let goodsModel = Goods.find(params).skip(skip).limit(pageSize);
  goodsModel.sort({'salePrice':sort});
  goodsModel.exec({},function (err,doc) {
    if(err){
      res.json({
        status:"1",
        msg:err.message
      });

    }else{
      res.json({
        status:'0',
        msg:'',
        result:{
          count:doc.length,
          list:doc
        }

      });

    }

  });


  //查询数据库
  // Goods.find({},function (err,doc) {
  //   if(err){
  //     res.json({
  //       status:"1",
  //       msg:err.message
  //     });
  //   }else{
  //     res.json({
  //       status:"0",
  //       msg:'',
  //       result:{
  //         count:doc.length,
  //         list:doc
  //       }
  //     })
  //   }
  // })
});
//加入购物车
router.post('/addCart',(req,res,next)=>{
    //拿到当前的用户  这里假设已经登录  productId得到前端传递来的productId
    var userId = '100000077',productId = req.body.productId;
    var User = require('../models/user');

    //获取用户信息
    User.findOne({
      //第一个是查询的参数，第二个是回调函数
      userId:userId},(err,userDoc)=>{
        if(err){
          res.json({
            status:'1',
            msg:err.message

          });

        }else{
          //console.log('userDoc:'+userDoc);

          if(userDoc){
            //遍历userDoc,看要加入的商品的id和购物车里的商品id是否有重复
            let goodsItem = '';
            userDoc.cartList.forEach((item,index)=>{
              if(item.productId == productId){
                goodsItem = item;
                item.productNum ++;

              }
            });
            if(goodsItem){
              userDoc.save((err2,doc2)=>{

                if(err2) {
                  console.log('失败------');
                  res.json({
                    status: '1',
                    msg: err2.message
                  });

                }else{
                  console.log('成功-----------');
                  res.json({
                    status:'0',
                    msg:'',
                    result:'success'
                  });

                }
              });
            }else{
              Goods.findOne({productId:productId},(err1,doc)=>{
                if(err1) {
                  res.json({
                    status: '1',
                    msg: err.message
                  });
                }else{
                  if(doc){
                    console.log(doc+'1111111111111111111');

                    doc.productNum = 1;
                    doc.checked = '1';


                    console.log(doc+'222222222222222');
                    userDoc.cartList.push(doc);

                    userDoc.save((err2,doc2)=>{

                      if(err2) {
                        console.log('失败没加入proeuctdNum------');
                        res.json({
                          status: '1',
                          msg: err2.message
                        });

                      }else{
                        console.log('成功-----------');
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
            }

          }
        }
    })

});
//输出
module.exports = router;
