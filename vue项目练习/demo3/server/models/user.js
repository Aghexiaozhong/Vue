var mongoose = require('mongoose');
// var User = require('./../models/user');  //获取uuser模型

var userSchema = new mongoose.Schema({
  "userId":String,
  "userName":String,
  "userPwd":String,
  "orderList":Array,
  "cartList":[
    {
      "productId": String,
      "productName": String,
      "salePrice": String,
      "productImage": String,
      "checked":String,
      "productNum":Number
    }

  ],
  "addressList":[{
      "addressId":String,
    "userName":String,
    "streetName":String,
    "postCode":Number,
    "tel":Number,
    "isDefault":Boolean
  }]


});




//数据库对应的集合要带s  比如users
module.exports = mongoose.model('User',userSchema);



