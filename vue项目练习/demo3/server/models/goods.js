var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var productSchema = new Schema({
  "productId":String,
  "productName":String,
  "salePrice":Number,
  "productImage":String,
  "productNum":Number,
  "checked":String
});
//这里写  Good 会联系到goods表
module.exports = mongoose.model('Good',productSchema);
